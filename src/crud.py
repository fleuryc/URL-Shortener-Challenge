"""CRUD package

Defines Create, Read, Update and Delete database operations.
"""
from sqlalchemy.orm import Session

from . import models, schemas


def get_short_by_key(db: Session, key: str) -> models.Short | None:
    """Get Short by key

    Select in database the first Short with matching key attribute.

    Args:
        db (Session): current database connexion
        key (str): key of the Short to select

    Returns:
        models.Short | None: Selected Short if there is a match, or None otherwise
    """
    return db.query(models.Short).filter(models.Short.key == key).first()


def get_short_by_url(db: Session, url: str) -> models.Short | None:
    """Get Short by url

    Select in database the first Short with matching url attribute.

    Args:
        db (Session): current database connexion
        url (str): url of the Short to select

    Returns:
        models.Short | None: Selected Short if there is a match, or None otherwise
    """
    return db.query(models.Short).filter(models.Short.url == url).first()


def create_short(db: Session, short: schemas.Short) -> models.Short:
    """Create a new Short

    Inserts a new Short in database, comit and refresh.

    Args:
        db (Session): current database connexion
        short (schemas.Short): new Short to insert

    Returns:
        models.Short: Inserted Short
    """
    db_short = models.Short(**short.dict())
    db.add(db_short)
    db.commit()
    db.refresh(db_short)
    return db_short
