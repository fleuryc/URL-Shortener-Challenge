"""Main package."""

from textwrap import dedent

from fastapi import FastAPI
from pydantic import AnyUrl, BaseModel, parse_obj_as


class ShortUrl(BaseModel):
    key: str
    url: AnyUrl

    class Config:
        orm_mode = True


app = FastAPI(
    title="URL Shortener API",
    description=dedent(
        """\
            This API allows you to :
            - create, store and return a unique key from a URL (`POST` : `/?url={url}`)
            - retrieve the corresponding URL from a unique key (`GET` : `/{key}`)
    """
    ),
    version="0.0.1",
)


@app.post("/", response_model=str)
def shorten_url(url: AnyUrl) -> str:
    """Shorten a URL

    - check if URL is already in database
      - yes => return corresponding unique key
      - no =>
        - create new ShortUrl
        - store in database
        - return corresponding unique key

    Args:
        url (AnyUrl): URL to be shortened

    Returns:
        str: unique key corresponding to the shortened URL
    """

    key = "fleuryc"
    return key


@app.get("/{key}", response_model=AnyUrl)
def get_url(key: str) -> AnyUrl:
    """Retrieve the corresponding URL from a unique key

    - check if the key exists in database
      - yes => return the corresponding URL
      - no => throw a 404 error

    Args:
        key (str): unique key corresponding to the shortened URL

    Returns:
        AnyUrl: original URL
    """

    url = parse_obj_as(AnyUrl, "https://www.clementfleury.me")
    return url
