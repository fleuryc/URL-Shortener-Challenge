"""Schemas package

Defines Pydantic validation model : Short
"""
from pydantic import BaseModel, Field, HttpUrl


class Short(BaseModel):
    # key is a random non-empty string composed of uppercas and lowercase characters, and digits
    key: str = Field(regex=r"^[a-zA-Z0-9]+$", example="fleuryc")
    # url must be a valid HTTP(s) URL
    url: HttpUrl = Field(example="https://www.clementfleury.me")

    class Config:
        schema_extra = {
            "example": {
                "key": "fleuryc",
                "url": "https://www.clementfleury.me",
            }
        }
        # ORM mode : to support models creation from any object
        orm_mode = True
