from __future__ import annotations

from enum import Enum

import attrs


class TextEmbeddingModel(str, Enum):
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"
    MXBAI_EMBED_LARGE_v1 = "mixedbread-ai/mxbai-embed-large-v1"
    BGE_LARGE_EN_v1_5 = "BAAI/bge-large-en-v1.5"
    BGE_BASE_EN_v1_5 = "BAAI/bge-base-en-v1.5"
    BGE_SMALL_EN_v1_5 = "BAAI/bge-small-en-v1.5"
    GTE_LARGE = "thenlper/gte-large"
    GTE_BASE = "thenlper/gte-base"
    GTE_GTE_SMALL = "thenlper/gte-small"
    SNOWFLAKE_ARCTIC_EMBED_XS = "Snowflake/snowflake-arctic-embed-xs"
    SNOWFLAKE_ARCTIC_EMBED_S = "Snowflake/snowflake-arctic-embed-s"
    SNOWFLAKE_ARCTIC_EMBED_M = "Snowflake/snowflake-arctic-embed-m"
    SNOWFLAKE_ARCTIC_EMBED_L = "Snowflake/snowflake-arctic-embed-l"
    E5_LARGE_UNSUPERVISED = "intfloat/e5-large-unsupervised"
    E5_BASE_UNSUPERVISED = "intfloat/e5-base-unsupervised"
    E5_SMALL_UNSUPERVISED = "intfloat/e5-small-unsupervised"


@attrs.frozen
class TextEmbeddingInferenceConfig:
    input_column: str
    output_column: str
    model: TextEmbeddingModel
