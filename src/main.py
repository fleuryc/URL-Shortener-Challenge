"""Main package."""

import logging
from textwrap import dedent

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from pydantic import HttpUrl
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud, models, schemas, utils
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(
    title="URL Shortener API",
    description=dedent(
        """\
            This API allows you to :
            - create, store and return a unique key from a URL (`POST` : `/?long_url={long_url}`)
            - retrieve the corresponding URL from a unique key (`GET` : `/{key}`)
    """
    ),
    version="1.0.0",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=schemas.Short)
def shorten(
    url: HttpUrl = Query(example="https://www.clementfleury.me"),
    db: Session = Depends(get_db),
) -> models.Short:
    """Shorten a URL

    Keys are randomly composed of :
      - lowercase characters [a-z]
      - uppercase characters [A-Z]
      - digits [0-9]

    Start with `key_length` = 1
    Infinite loop :
    - check if URL is already in database
      - yes => return corresponding unique key
      - no =>
        - generate a new key of size `key_length`
        - create and try to store in Database the Short
        - check if save was successful
          - yes => return the Short
          - no => increment key length and try again!

    This algorithm statistically ensures that the keys are :
    - (almost) as short as possible
    - random
    - unique, while minimizing the number of database requests to ensure unicity

    @WARNING : This might throw HTTP "508 Loop Detected" error in case of really really bad luck !

    Args:
        url (HttpUrl): URL to be shortened.
        db (Session): database session.

    Returns:
        models.Short: new Short with unique key.
    """
    # start with the smallest key
    key_length = 1
    while True:
        if db_short := crud.get_short_by_url(db, url):
            # URL already shortened => return the Short
            return db_short

        # new URL to shorten => generate a key of size `key_length`
        key = utils.generate_key(key_length)
        # create a new Short
        short = schemas.Short(key=key, url=url)
        try:
            # try to save the new Short and return if successful
            return crud.create_short(db, short)
        except IntegrityError as e:
            # if key or URL already exist (unique constraint)
            # log a warning
            logging.warning(e)
            # rollback the insert
            db.rollback()
            # increment the key size
            key_length += 1


@app.get("/{key}", response_model=schemas.Short)
def get_url(
    key: str = Path(example="fleuryc"), db: Session = Depends(get_db)
) -> models.Short:
    """Retrieve the corresponding Short from a unique key

    - check if the key exists in database
      - yes => return the corresponding URL
      - no => throw a 404 error

    Args:
        key (str): unique key corresponding to the shortened URL.
        db (Session): database session.

    Raises:
        HTTPException: 404 error if no Short match the given key

    Returns:
        models.Short: retrieved Short
    """

    if db_short := crud.get_short_by_key(db, key):
        # URL already shortened => return the Short
        return db_short

    # no Short corresponding to the provided key => 404 HTTP error
    raise HTTPException(status_code=404, detail="Short not found")
