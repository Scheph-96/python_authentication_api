import unicodedata

from pydantic import BaseModel, field_validator


class BaseSchema(BaseModel):
    """
        Common sanitization for all schemas.
    """

    @field_validator("*", mode="before")
    @classmethod
    def sanitize_strings(cls, v):
        if not isinstance(v, str):
            return v

        # Unicode normalization (security + consistency)
        v = unicodedata.normalize("NFKC", v)

        # Remove invisible characters (zero-width space)
        v = v.replace("\u200b", "")

        # Normalize line endings
        v = v.replace("\r\n", "\n")

        # Trim whitespace
        return v.strip()

    # Reject empty strings. "" or " "
    @field_validator("*")
    @classmethod
    def validate(cls, v):
        if v is not None and not v:
            raise ValueError("Field cannot be empty")
        return v

    model_config = {
        "extra": "forbid", # reject unknown fields
        "str_strip_whitespace": False, # we control trimming ourselves
    }
