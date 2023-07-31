from typing import TypedDict


class RetrieveMediaEvent(TypedDict):
    pathParameters: dict[str, str]
    queryStringParameters: dict[str, str]
