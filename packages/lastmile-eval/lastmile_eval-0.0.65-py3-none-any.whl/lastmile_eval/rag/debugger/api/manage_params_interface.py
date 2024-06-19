"""
This file defines the OpinionatedParamsInterface, which is an interface for defining RAG-specific parameters.

The LastMileTracer class in the lastmile_tracer.py file inherits from the OpinionatedParamsImpl class,
which is the implementation of the OpinionatedParamsInterface defined in the opinionated_params_impl.py file.

The LastMileTracer API in the tracing.py file inherits from this OpinionatedParamsInterface.

This structure allows for a clear separation of the interface and its implementation, while providing
a convenient way to access the RAG-specific parameters through the LastMileTracer API.
"""

import abc
from typing import Any, Optional

from opentelemetry.trace.span import Span


class ManageParamsInterface(abc.ABC):
    """
    Interface for defining the RAG-specific Params.
    """

    @abc.abstractmethod
    def register_query_model(
        self,
        value: str,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Register the model used by the query for the current trace instance.

        Args:
            value (str): The value of the query model parameter.
            should_also_save_in_span (bool): Flag indicating if the parameter should also be saved in the span. Defaults to True.
            span (Optional[Span]): The span to associate with the parameter. Defaults to None.

        Example:
            >>> tracer.register_query_model("gpt-4")
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def register_query_temperature(
        self,
        value: float,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Register the query temperature for the current trace instance.

        Args:
            value (float): The value of the query temperature.
            should_also_save_in_span (bool): Flag indicating if the parameter should also be saved in the span. Defaults to True.
            span (Optional[Span]): The span to associate with the parameter. Defaults to None.

        Example:
            >>> tracer.register_query_temperature(0.7)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def register_query_top_p(
        self,
        value: float,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Register the query top_p value for the current trace instance.

        Args:
            value (float): The value of the query top_p parameter.
            should_also_save_in_span (bool): Flag indicating if the parameter should also be saved in the span. Defaults to True.
            span (Optional[Span]): The span to associate with the parameter. Defaults to None.

        Example:
            >>> tracer.register_query_top_p(0.9)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def register_ingestion_chunk_size(
        self,
        value: int,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Register the ingestion chunk size for the current trace instance.

        Args:
            value (int): The value of the ingestion chunk size.
            should_also_save_in_span (bool): Flag indicating if the parameter should also be saved in the span. Defaults to True.
            span (Optional[Span]): The span to associate with the parameter. Defaults to None.

        Example:
            >>> tracer.register_ingestion_chunk_size(100)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def register_retrieval_top_k(
        self,
        value: int,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Register the retrieval top_k value for the current trace instance.

        Args:
            value (int): The value of the retrieval top_k parameter.
            should_also_save_in_span (bool): Flag indicating if the parameter should also be saved in the span. Defaults to True.
            span (Optional[Span]): The span to associate with the parameter. Defaults to None.

        Example:
            >>> tracer.register_retrieval_top_k(10)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def register_param(
        self,
        key: str,
        value: Any,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Define the parameter K-V pair to save for the current trace instance.

        If this is called outside of an active trace, it will save this into
        a global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)

        @param key (str): The name of the parameter to be saved
        @param value (Any): The value of the parameter to be saved
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def get_params(self) -> dict[str, Any]:
        """
        Returns the params_dict that contains all the parameters that have been
        registered with a trace so far.

        If this is called outside of an active trace, it will return the
        global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def register_params(
        self,
        params: dict[str, Any],
        should_overwrite: bool = False,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Helper function for individually calling `register_param`, with the
        added capability of clearing existing parameters if they exist.

        If this is called outside of an active trace, it will save these into
        a global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)

        @param params dict[str, Any]: The parameter K-V pairs to save
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param should_overwrite (bool): Whether to clear existing parameters
            if they already exist. Defaults to false.
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span

        Define the parameter K-V pair to save for the current trace instance
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def clear_params(
        self,
        should_clear_global_params: bool = False,
    ) -> None:
        """
        Clearing all existing parameters for the current trace instance.

        If this is called outside of an active trace, it will only clear the
        global params dict if `should_clear_global_params` is set to True.

        @param should_clear_global_params (bool): Whether to clear the global
        K-V pairs in addition to the current trace params. Defaults to false
        """
        raise NotImplementedError("Not implemented directly, this is an API")
