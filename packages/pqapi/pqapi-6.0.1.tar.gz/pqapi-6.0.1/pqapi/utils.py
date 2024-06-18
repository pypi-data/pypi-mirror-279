import os


def get_pqa_key() -> str:
    if "PQA_API_KEY" in os.environ:
        return os.environ["PQA_API_KEY"]
    if "PQA_API_TOKEN" in os.environ:
        return os.environ["PQA_API_TOKEN"]
    raise KeyError("PQA_API_KEY environment variable not set.")


def get_pqa_url() -> str:
    return os.environ.get("PQA_URL", "https://prod.api.paperqa.app")
