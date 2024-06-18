import logging
from typing import Any, BinaryIO
from uuid import UUID

import aiohttp
import requests
import tenacity
from paperqa.types import Answer
from pydantic import BaseModel

from .models import (
    DocsStatus,
    QueryRequest,
    QueryRequestMinimal,
    UploadMetadata,
)
from .utils import get_pqa_key, get_pqa_url

logger = logging.getLogger(__name__)
PQA_URL = get_pqa_url()


def coerce_request(
    query: str | QueryRequest, named_template: str | None
) -> QueryRequest | QueryRequestMinimal:
    if isinstance(query, str):
        return QueryRequestMinimal(query=query, named_template=named_template)
    if isinstance(query, QueryRequest):
        return query
    raise TypeError("Query must be a string or QueryRequest")


class AnswerResponse(BaseModel):
    answer: Answer
    usage: dict[str, list[int]]
    bibtex: dict[str, str]
    status: str
    timing_info: dict[str, dict[str, float]] | None = None
    duration: float = 0

    async def save_as_template(self, name: str, public: bool = False):
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{PQA_URL}/api/templates/create/{name}",
                params={"query_id": str(self.answer.id), "public": str(public)},
                timeout=30,
                headers={"Authorization": f"Bearer {get_pqa_key()}"},
            ) as response,
        ):
            response.raise_for_status()


def parse_response(data: dict[str, Any]) -> AnswerResponse:
    return AnswerResponse(**data)


def upload_file(
    bibliography: str,
    file: BinaryIO,
    metadata: UploadMetadata,
    public: bool = False,
) -> dict[str, Any]:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"

    with requests.Session() as session:
        response = session.post(
            f"{PQA_URL}/api/docs/{bibliography}/upload",
            files=[("file", file)],
            json={"metadata": metadata.model_dump()},
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        return response.json()


def upload_paper(doi: str, file: BinaryIO) -> None:
    with requests.Session() as session:
        result = session.post(
            f"{PQA_URL}/db/upload/paper/",
            params={"doi": doi},
            files=[("file", file)],
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        result.raise_for_status()


def check_dois(dois: list[str]) -> dict[str, tuple[str, str]]:
    with requests.Session() as session:
        result = session.post(
            f"{PQA_URL}/db/docs/dois",
            json=dois,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        result.raise_for_status()
        return result.json()


def delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/db/docs/delete/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()


async def async_delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/db/docs/delete/{bibliography}"
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()


def get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/status/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        return DocsStatus(**response.json())


async def async_get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public and not bibliography.startswith("public:"):
        bibliography = f"public:{bibliography}"
    url = f"{PQA_URL}/api/docs/status/{bibliography}"
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        data = await response.json()
        return DocsStatus(**data)


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=30),
    stop=tenacity.stop_after_attempt(3),
)
def agent_query(
    query: QueryRequest | str,
    bibliography: str = "tmp",
    named_template: str | None = None,
) -> AnswerResponse:
    query_request = coerce_request(query, named_template)
    url = f"{PQA_URL}/api/agent/{bibliography if bibliography else 'tmp'}"
    with requests.Session() as session:
        response = session.post(
            url,
            json=query_request.model_dump(),
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        return parse_response(response.json())


@tenacity.retry(
    wait=tenacity.wait_random_exponential(multiplier=1, max=10),
    stop=tenacity.stop_after_attempt(2),
)
async def async_agent_query(
    query: QueryRequest | str,
    bibliography: str = "tmp",
    named_template: str | None = None,
) -> AnswerResponse:
    query_request = coerce_request(query, named_template)
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            f"{PQA_URL}/api/agent/{bibliography if bibliography else 'tmp'}",
            json=query_request.model_dump(),
            timeout=1200,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        try:
            data = await response.json()
        except Exception:
            text = await response.text()
            logger.warning(
                f"Failed Request: \n{query_request.model_dump_json(indent=2)}"
            )
            logger.warning(f"\n\nResponse:\n\n{text}")
        response.raise_for_status()
        return parse_response(data)


async def async_send_feedback(
    queries: list[UUID], feedback: list[dict], group: str | None = None
) -> bool:
    url = f"{PQA_URL}/api/feedback"
    # default JSON serializer in python cannot handle UUID
    queries_as_str = [str(q) for q in queries]
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            url,
            json={
                "queries": queries_as_str,
                "feedback": feedback,
                "feedback_group": group,
            },
            timeout=600,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
    return True


async def async_get_feedback(
    query: UUID | None = None, group: str | None = None
) -> dict[str, Any]:
    # add as query parameters
    body = {"query": str(query), "feedback_group": group}
    if query is None and group is None:
        raise ValueError("At least one of query or group must be provided")
    if query is None:
        del body["query"]
    if group is None:
        del body["feedback_group"]
    url = f"{PQA_URL}/db/feedback"

    async with (
        aiohttp.ClientSession() as session,
        session.get(
            url,
            json=body,
            timeout=600,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        ) as response,
    ):
        response.raise_for_status()
        return await response.json()
