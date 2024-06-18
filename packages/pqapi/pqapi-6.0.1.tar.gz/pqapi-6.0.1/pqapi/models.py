import re
from enum import Enum
from typing import Any

import paperqa
from paperqa.types import PromptCollection
from pydantic import BaseModel, Field, ValidationInfo, field_validator, validator


def _extract_doi(citation: str) -> str | None:
    doi = re.findall(r"10\.\d{4}/\S+", citation, re.IGNORECASE)
    if len(doi) > 0:
        return doi[-1]
    return None


class UploadMetadata(BaseModel):
    filename: str
    citation: str
    key: str | None = None


class Doc(paperqa.Doc):
    doi: str | None = None

    @validator("doi", pre=True)
    def citation_to_doi(cls, v: str | None, values: dict) -> str | None:  # noqa: N805
        if v is None and "citation" in values:
            return _extract_doi(values["citation"])
        return v


class DocsStatus(BaseModel):
    name: str
    llm: str
    summary_llm: str
    docs: list[Doc]
    doc_count: int
    writeable: bool = False


class QueryRequestMinimal(BaseModel):
    """A subset of the fields in the QueryRequest model."""

    query: str = Field(..., description="The query to be answered")
    group: str | None = Field(None, description="A way to group queries together")
    named_template: str | None = Field(
        None,
        description="The template to be applied (if any) to the query for settings things like models, chunksize, etc.",
    )


# COPIED FROM paperqa-server!
class ParsingOptions(str, Enum):
    S2ORC = "s2orc"
    PAPERQA_DEFAULT = "paperqa_default"
    GROBID = "grobid"


class ChunkingOptions(str, Enum):
    SIMPLE_OVERLAP = "simple_overlap"
    SECTIONS = "sections"


class ParsingConfiguration(BaseModel):
    """Holds a superset of params and methods needed for each algorithm."""

    # the below will always fall back to the paperqa-default parser, even if not specified
    ordered_parser_preferences: list[ParsingOptions] = [
        ParsingOptions.S2ORC,
        ParsingOptions.PAPERQA_DEFAULT,
    ]
    chunksize: int = 6000
    overlap: int = 100
    chunking_algorithm: ChunkingOptions = ChunkingOptions.SIMPLE_OVERLAP


# NOTE AGENT PROMPT COLLECTION IS NOT HERE!
# Haven't required it yet
class QueryRequest(BaseModel):
    query: str
    group: str | None = None
    llm: str = "gpt-4-0613"
    summary_llm: str = "gpt-3.5-turbo-0125"
    length: str = "about 200 words, but can be longer if necessary"
    summary_length: str = "about 100 words"
    max_sources: int = 7
    consider_sources: int = 12
    # if you change this to something other than default
    # modify code below in update_prompts
    prompts: PromptCollection = Field(default_factory=PromptCollection)
    texts_index_mmr_lambda: float = 0.9
    docs_index_mmr_lambda: float = 0.5
    # concurrent number of summary calls to use inside Doc object
    max_concurrent: int = 12
    temperature: float = 0.0
    summary_temperature: float = 0.0
    docs_index_embedding_config: dict[str, Any] | None = None
    parsing_configuration: ParsingConfiguration = Field(
        default_factory=ParsingConfiguration
    )
    embedding: str = "hybrid-text-embedding-3-small"
    # at what size should we start using adoc_match?
    adoc_match_threshold: int = 500
    # Should we filter out "Extra Background Information" citations
    # which come from pre-step in paper-qa algorithm
    filter_extra_background: bool = True

    @field_validator("prompts")
    def treat_summary_llm_none(
        cls,  # noqa: N805
        v: PromptCollection,
        info: ValidationInfo,
    ) -> PromptCollection:
        values = info.data
        if values["summary_llm"] == "none":
            v.skip_summary = True
            # for simplicity (it is not used anywhere)
            # so that Docs doesn't break when we don't have a summary_llm
            values["summary_llm"] = "gpt-3.5-turbo"
        return v
