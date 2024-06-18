"""
Implementation of the OpinionatedParams interface for defining the RAG-specific params.
"""

from enum import Enum
from typing import Optional

from opentelemetry.trace import Span

from lastmile_eval.rag.debugger.api.tracing import LastMileTracer


class OpinionatedParamKey(Enum):
    """
    Opinionated parameter keys for the RAG-specific parameters.
    """

    QUERY_MODEL = "query_model"
    QUERY_TEMPERATURE = "query_temperature"
    QUERY_TOP_P = "query_top_p"
    INGESTION_CHUNK_SIZE = "ingestion_chunk_size"
    RETRIEVAL_TOP_K = "retrieval_top_k"


class ManageParamsImpl(LastMileTracer):
    """
    Implementation of the OpinionatedParams interface for defining the RAG-specific events.
    """

    def register_query_model(
        self,
        value: str,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        See `lastmile_eval.rag.debugger.api.ManageParamsInterface.register_query_model()`
        """
        self.register_param(
            OpinionatedParamKey.QUERY_MODEL.value,
            value,
            span=span,
            should_also_save_in_span=should_also_save_in_span,
        )

    def register_query_temperature(
        self,
        value: float,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        See `lastmile_eval.rag.debugger.api.ManageParamsInterface.register_query_temperature()`
        """
        self.register_param(
            OpinionatedParamKey.QUERY_TEMPERATURE.value,
            value,
            span=span,
            should_also_save_in_span=should_also_save_in_span,
        )

    def register_query_top_p(
        self,
        value: float,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        See `lastmile_eval.rag.debugger.api.ManageParamsInterface.register_retrieval_top_k()`
        """
        self.register_param(
            OpinionatedParamKey.QUERY_TOP_P.value,
            value,
            span=span,
            should_also_save_in_span=should_also_save_in_span,
        )

    def register_retrieval_top_k(
        self,
        value: int,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        See `lastmile_eval.rag.debugger.api.ManageParamsInterface.register_retrieval_top_k()`
        """
        self.register_param(
            OpinionatedParamKey.RETRIEVAL_TOP_K.value,
            value,
            span=span,
            should_also_save_in_span=should_also_save_in_span,
        )

    def register_ingestion_chunk_size(
        self,
        value: int,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        See `lastmile_eval.rag.debugger.api.ManageParamsInterface.register_ingestion_chunk_size()`
        """
        self.register_param(
            OpinionatedParamKey.INGESTION_CHUNK_SIZE.value,
            value,
            span=span,
            should_also_save_in_span=should_also_save_in_span,
        )
