import logging
import os
from typing import Callable, Generator, Mapping, Optional, Sequence

import numpy as np
import pandas as pd
import requests
import result
from requests import Response

from lastmile_eval.rag.debugger.common import core

from ..offline_evaluation import evaluation_lib
from ..offline_evaluation.evaluation_lib import (
    BatchDownloadParams,
    BatchOutputsWithOTELTraceIds,
    clean_rag_query_tracelike_df,
    wrap_with_tracer,
)

logger = logging.getLogger(__name__)
logging.basicConfig()


# TODO(b7r6): probably move these definitions to a common module
# that's accessible to both our code and user code
Evaluator = evaluation_lib.Evaluator
AggregatedEvaluator = evaluation_lib.AggregatedEvaluator
SaveOptions = evaluation_lib.SaveOptions


WEBSITE_BASE_URL = "https://lastmileai.dev"


def list_example_sets(
    take: int = 10,
    timeout: int = 60,
    lastmile_api_token: Optional[str] = None,
) -> core.JSONObject:
    """
    Get a list of test sets from the LastMile API.

    Args:
        take: The number of test sets to return. The default is 10.
        lastmile_api_token: The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            {WEBSITE_BASE_URL}/settings?page=tokens
        timeout: The maximum time in seconds to wait for the request to complete.
            The default is 60.

    Returns:
        A dictionary containing the test sets.
    """
    lastmile_api_token = core.token(lastmile_api_token)
    endpoint_with_params = f"evaluation_example_sets/list?pageSize={str(take)}"
    lastmile_url = os.path.join(WEBSITE_BASE_URL, "api", endpoint_with_params)

    response: Response = requests.get(
        lastmile_url,
        headers={"Authorization": f"Bearer {lastmile_api_token}"},
        timeout=timeout,
    )
    # TODO(jll): Handle response errors
    return response.json()


def download_input_traces(
    project_name: Optional[str] = None,
    trace_id: Optional[str] = None,
    batch_limit: Optional[int] = None,
    substring_filter: Optional[str] = None,
    creator_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    lastmile_api_token: Optional[str] = None,
) -> Generator[pd.DataFrame, None, None]:
    HARD_BATCH_LIMIT = 50
    if batch_limit is None:
        batch_limit = HARD_BATCH_LIMIT

    if batch_limit < 1 or batch_limit > HARD_BATCH_LIMIT:
        raise ValueError(
            f"batch_limit must be between 1 and {HARD_BATCH_LIMIT}"
        )

    base_url = WEBSITE_BASE_URL
    lastmile_api_token = core.token(lastmile_api_token)
    project_id = (
        evaluation_lib.get_project_id_from_name(
            base_url=core.BaseURL(base_url),
            project_name=core.ProjectName(project_name),
            lastmile_api_token=core.APIToken(lastmile_api_token),
        )
        if project_name is not None
        else result.Ok(None)
    )

    download_params: core.Res[BatchDownloadParams] = result.do(
        result.Ok(
            BatchDownloadParams(
                batch_limit=batch_limit,
                search=substring_filter,
                trace_id=(
                    core.RAGQueryTraceID(trace_id)
                    if trace_id is not None
                    else None
                ),
                creator_id=(
                    core.CreatorID(creator_id)
                    if creator_id is not None
                    else None
                ),
                project_id=project_id_ok,
                organization_id=(
                    core.OrganizationID(organization_id)
                    if organization_id is not None
                    else None
                ),
                start_timestamp=start_time,
                end_timestamp=end_time,
            )
        )
        for project_id_ok in project_id
    )

    generator = result.do(
        evaluation_lib.download_rag_query_traces_helper(
            core.BaseURL(base_url),
            core.APIToken(lastmile_api_token),
            download_params_ok,
        )
        for download_params_ok in download_params
    )

    match (generator):
        case result.Ok(generator_ok):
            for batch in generator_ok:
                yield batch.map(clean_rag_query_tracelike_df).unwrap_or_raise(
                    ValueError
                )
        case result.Err(e):
            raise ValueError(e)


def download_rag_events(
    project_name: Optional[str] = None,
    batch_limit: Optional[int] = None,
    substring_filter: Optional[str] = None,
    creator_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    event_name: Optional[str] = None,
    lastmile_api_token: Optional[str] = None,
) -> Generator[pd.DataFrame, None, None]:
    HARD_BATCH_LIMIT = 50
    if batch_limit is None:
        batch_limit = HARD_BATCH_LIMIT

    if batch_limit < 1 or batch_limit > HARD_BATCH_LIMIT:
        raise ValueError(
            f"batch_limit must be between 1 and {HARD_BATCH_LIMIT}"
        )
    base_url = WEBSITE_BASE_URL
    lastmile_api_token = core.token(lastmile_api_token)
    project_id = (
        evaluation_lib.get_project_id_from_name(
            base_url=core.BaseURL(base_url),
            project_name=core.ProjectName(project_name),
            lastmile_api_token=core.APIToken(lastmile_api_token),
        )
        if project_name is not None
        else result.Ok(None)
    )

    download_params: core.Res[BatchDownloadParams] = result.do(
        result.Ok(
            BatchDownloadParams(
                batch_limit=batch_limit,
                search=substring_filter,
                creator_id=(
                    core.CreatorID(creator_id)
                    if creator_id is not None
                    else None
                ),
                project_id=project_id_ok,
                organization_id=(
                    core.OrganizationID(organization_id)
                    if organization_id is not None
                    else None
                ),
                start_timestamp=start_time,
                end_timestamp=end_time,
                event_name=event_name,
            )
        )
        for project_id_ok in project_id
    )

    generator = result.do(
        evaluation_lib.download_rag_events_helper(
            core.BaseURL(base_url),
            core.APIToken(lastmile_api_token),
            download_params_ok,
        )
        for download_params_ok in download_params
    )

    match (generator):
        case result.Ok(generator_ok):
            for batch in generator_ok:
                yield batch.unwrap_or_raise(ValueError)
        case result.Err(e):
            raise ValueError(e)


def create_input_set(
    queries: Sequence[str] | pd.DataFrame,
    project_name: Optional[str] = None,
    input_set_name: Optional[str] = None,
    ground_truths: Optional[list[str]] = None,
    lastmile_api_token: Optional[str] = None,
) -> evaluation_lib.CreateInputSetResponse:
    """
    Create an Input set from a list of strings.

    lastmile_api_token: The API token for the LastMile API. If not provided,
        will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    """
    base_url = WEBSITE_BASE_URL
    lastmile_api_token = core.token(lastmile_api_token)

    project_id = (
        evaluation_lib.get_project_id_from_name(
            base_url=core.BaseURL(base_url),
            project_name=core.ProjectName(project_name),
            lastmile_api_token=core.APIToken(lastmile_api_token),
        )
        if project_name is not None
        else result.Ok(None)
    )

    outcome = result.do(
        evaluation_lib.create_input_set_helper(
            core.BaseURL(base_url),
            project_id_ok,
            queries,
            core.APIToken(lastmile_api_token),
            input_set_name,
            ground_truths,
        )
        for project_id_ok in project_id
    )

    return outcome.unwrap_or_raise(ValueError)


def download_input_set(
    input_set_id: Optional[str] = None,
    input_set_name: Optional[str] = None,
    lastmile_api_token: Optional[str] = None,
) -> pd.DataFrame:
    base_url = WEBSITE_BASE_URL
    lastmile_api_token = core.token(lastmile_api_token)

    outcome = evaluation_lib.download_input_set_helper(
        core.BaseURL(base_url),
        core.InputSetID(input_set_id) if input_set_id is not None else None,
        input_set_name,
        lastmile_api_token,
    )

    return outcome


def create_example_set(
    df: pd.DataFrame,
    example_set_name: Optional[str],
    project_name: Optional[str] = None,
    ground_truths: Optional[list[str]] = None,
    lastmile_api_token: Optional[str] = None,
) -> evaluation_lib.CreateExampleSetResponse:
    base_url = WEBSITE_BASE_URL
    lastmile_api_token = core.token(lastmile_api_token)

    project_id = (
        evaluation_lib.get_project_id_from_name(
            base_url=core.BaseURL(base_url),
            project_name=core.ProjectName(project_name),
            lastmile_api_token=core.APIToken(lastmile_api_token),
        )
        if project_name is not None
        else result.Ok(None)
    )

    outcome = result.do(
        evaluation_lib.create_example_set_helper(
            core.BaseURL(base_url),
            project_id_ok,
            df,
            example_set_name,
            ground_truths,
            core.APIToken(lastmile_api_token),
        )
        for project_id_ok in project_id
    )
    return outcome.unwrap_or_raise(ValueError)


def download_example_set(
    example_set_id: Optional[str] = None,
    example_set_name: Optional[str] = None,
    lastmile_api_token: Optional[str] = None,
) -> pd.DataFrame:
    base_url = WEBSITE_BASE_URL
    lastmile_api_token = core.token(lastmile_api_token)

    raw = evaluation_lib.download_example_set_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        (
            core.ExampleSetID(example_set_id)
            if example_set_id is not None
            else None
        ),
        example_set_name,
    )

    return raw.map(clean_rag_query_tracelike_df).unwrap_or_raise(ValueError)


def run_query_function(
    run_query_fn: Callable[[str], str],
    inputs: Sequence[str] | pd.DataFrame,
    project_name: Optional[str] = None,
) -> list[str]:
    run_query_with_tracer_fn = wrap_with_tracer(
        run_query_fn, project_name=project_name
    )

    def _extract_first_from_user_outputs(
        the_tuple: BatchOutputsWithOTELTraceIds,
    ) -> list[str]:
        return the_tuple[0]

    outcome = evaluation_lib.run_rag_query_fn_helper(
        run_query_with_tracer_fn, inputs
    ).map(_extract_first_from_user_outputs)

    return outcome.unwrap_or_raise(ValueError)


def evaluate(
    project_name: Optional[str] = None,
    example_set_id: Optional[str] = None,
    examples_dataframe: Optional[pd.DataFrame] = None,
    evaluators: Optional[
        Mapping[
            str,
            Evaluator,
        ]
        | set[str]
    ] = None,
    aggregated_evaluators: Optional[
        Mapping[
            str,
            AggregatedEvaluator,
        ]
    ] = None,
    save_options: Optional[SaveOptions] = None,
    lastmile_api_token: Optional[str] = None,
) -> evaluation_lib.CreateEvaluationResponse:
    """
    *Description*

        Run evaluations on RAG query Examples using chosen evaluation functions.

        project_name: Optionally, this allows you to group your evaluation results with other evaluations within the project.
        example_set_id, examples_dataframe: give one of these to specify your evaluation inputs.
        evaluators: A mapping of evaluator names to evaluator functions. Each evaluator takes a DataFrame and produces one value per row.
            Example: {"exact_match": some_exact_match_checking_function}
        aggregated_evaluators: Like evaluators, but these functions take a DataFrame and produce a single value that aggregates over the entire input.

        save_options: Controls backend storage options for your Evaluation Result.

        lastmile_api_token: You can get one here https://lastmileai.dev/settings?page=tokens.
        If None, this function will try to load it from a local .env file.


    *Input Data (Examples)*

        A RAG query example is essentially a row of data
        containing fields like `query`, `context`, `prompt`, `groundTruth`, etc.

        Examples can contain any data from your RAG Query Traces, for example, as well as a groundTruth column.

        The data is specified as either an example set ID or a DataFrame. If an example set ID is provided,
        it will be downloaded from the LastMile API and evaluations will run locally.

        If a DataFrame is provided, it will be used directly (also locally).

    *Evaluators*

        Each evaluator is a function that maps a DataFrame to a list of metric values, one float per row.
        The idea is to apply an example-level evaluator to each row of the input DataFrame.

        Accepts either mapping of callable or a set of predefined default evaluator names.

        Aggregated evaluators allow you to do custom aggregations over all the DataFrame rows (for example, some specific recall@precision).
        If not provided, a few defaults will be used.



    """

    base_url = core.BaseURL(WEBSITE_BASE_URL)
    lastmile_api_token = core.token(lastmile_api_token)

    project_id = (
        evaluation_lib.get_project_id_from_name(
            base_url=core.BaseURL(base_url),
            project_name=core.ProjectName(project_name),
            lastmile_api_token=core.APIToken(lastmile_api_token),
        )
        if project_name is not None
        else result.Ok(None)
    )

    save_options_ = save_options or SaveOptions()

    all_typed_evaluators = (
        evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
            evaluators, aggregated_evaluators, lastmile_api_token
        )
    )

    outcome = result.do(
        evaluation_lib.evaluate_helper(
            base_url,
            project_id_ok,
            (
                core.ExampleSetID(example_set_id)
                if example_set_id is not None
                else None
            ),
            examples_dataframe,
            lastmile_api_token,
            save_options_,
            all_typed_evaluators_ok,
        )
        for project_id_ok in project_id
        for all_typed_evaluators_ok in all_typed_evaluators
    )

    return outcome.unwrap_or_raise(ValueError)


# TODO: Figure out how to specify we want to inputs and outputs from eventData
# for evaluators instead of default "input" and "output" columns
# We can also for now just say we don't support running eval on eventData and
# we must have defined inputs. I think this is reasonable
def run_and_evaluate(
    run_query_fn: Callable[[str], str],
    project_name: Optional[str] = None,
    input_set_id: Optional[str] = None,
    inputs: Optional[list[str]] = None,
    ground_truths: Optional[list[str]] = None,
    evaluators: Optional[
        Mapping[
            str,
            Evaluator,
        ]
        | set[str]
    ] = None,
    aggregated_evaluators: Optional[
        Mapping[
            str,
            AggregatedEvaluator,
        ]
    ] = None,
    save_options: Optional[SaveOptions] = None,
    n_trials: int = 1,
    lastmile_api_token: Optional[str] = None,
) -> evaluation_lib.CreateEvaluationResponse:
    """
    *Description*

        Run a RAG query flow function on the given inputs,
        then run evaluations on corresponding RAG query outputs using chosen evaluation functions.

        run_query_fn: This should run or simulate your RAG query flow. It must either return a string output,
            or a tuple (string, string) representing (output, rag_query_trace_id).
            If you return the tuple, the evaluation results will be connected to the trace in the UI.

        project_name: Optionally, this allows you to group your evaluation results with other evaluations within the project.
        input_set_id, inputs: give exactly one of these to specify your RAG system inputs (query time input).
        ground_truths: Optionally, provide ground truths (references) for each of your inputs.
            This is only accepted if you give a list for your inputs.
            If you give input_set_id, the library will fetch your ground truths from that input set and you must not give ground truths as a function argument.



        evaluators: A mapping of evaluator names to evaluator functions. Each evaluator takes a DataFrame and produces one value per row.
            Example: {"exact_match": some_exact_match_checking_function}
        aggregated_evaluators: Like evaluators, but these functions take a DataFrame and produce a single value that aggregates over the entire input.

        save_options: Controls backend storage options for your Example Set and Evaluation Result.

        n_trials: This allows you to simulate a larger Example sample set by using your RAG query inputs N times each.

        lastmile_api_token: You can get one here https://lastmileai.dev/settings?page=tokens.
        If None, this function will try to load it from a local .env file.


    *Input Data (Examples)*


    *Evaluators*

        See `evaluate()`.

    """

    base_url = core.BaseURL(WEBSITE_BASE_URL)
    lastmile_api_token = core.token(lastmile_api_token)

    project_id = (
        evaluation_lib.get_project_id_from_name(
            base_url=core.BaseURL(base_url),
            project_name=core.ProjectName(project_name),
            lastmile_api_token=core.APIToken(lastmile_api_token),
        )
        if project_name is not None
        else result.Ok(None)
    )

    save_options_ = save_options or SaveOptions()

    if not save_options_.do_save:
        raise ValueError(
            "do_save==False is currently not supported for `run_and_evaluate()`."
        )

    all_typed_evaluators = (
        evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
            evaluators, aggregated_evaluators, lastmile_api_token
        )
    )

    run_query_with_tracer_fn = wrap_with_tracer(
        run_query_fn, project_name=project_name
    )

    outcome = result.do(
        evaluation_lib.run_and_evaluate_helper(
            base_url,
            project_id_ok,
            run_query_with_tracer_fn,
            all_typed_evaluators_ok,
            save_options_,
            n_trials,
            lastmile_api_token,
            (
                core.InputSetID(input_set_id)
                if input_set_id is not None
                else None
            ),
            inputs,
            ground_truths,
        )
        for project_id_ok in project_id
        for all_typed_evaluators_ok in all_typed_evaluators
    )

    return outcome.unwrap_or_raise(ValueError)


def assert_is_close(
    evaluation_result: evaluation_lib.CreateEvaluationResponse,
    metric_name: str,
    value: float,
) -> None:
    df_metrics_agg = evaluation_result.df_metrics_aggregated
    metric = df_metrics_agg.set_index(["testSetId", "metricName"]).value.unstack("metricName")[metric_name].iloc[0]  # type: ignore[pandas]
    assert np.isclose(metric, value), f"Expected: {value}, Got: {metric}"  # type: ignore[fixme]


def get_default_evaluators(
    names: set[str], lastmile_api_token: Optional[str] = None
) -> dict[
    str,
    Evaluator,
]:
    lastmile_api_token = core.token(lastmile_api_token)

    return evaluation_lib.get_default_evaluators_helper(
        names, lastmile_api_token
    )
