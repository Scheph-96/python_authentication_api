import unicodedata

from pydantic import BaseModel, field_validator


class BaseSchema(BaseModel):
    """
        Common sanitization for all schemas.
    """

    @classmethod
    def _sanitize(cls, v):
        # ------- STRING -------
        if isinstance(v, str):
            # Unicode normalization (security + consistency)
            v = unicodedata.normalize("NFKC", v)

            # Remove invisible characters (zero-width space)
            v = v.replace("\u200b", "")

            # Normalize line endings
            v = v.replace("\r\n", "\n")

            # Trim whitespace
            v = v.strip()

            return v

        # ------- LIST -------
        if isinstance(v, list):
            return [cls._sanitize(item) for item in v]

        # ------- DICT -------
        if isinstance(v, dict):
            return {k: cls._sanitize(val) for k, val in v.items()}

        return v

    @classmethod
    def _validate(cls, v):
        # ------- STRING -------
        if isinstance(v, str):
            if not v:
                raise ValueError("Field cannot be empty")

        # ------- LIST -------
        elif isinstance(v, list):
            for item in v:
                cls._validate(item)

        # ------- DICT -------
        elif isinstance(v, dict):
            for val in v.values():
                cls._validate(val)

        return v

    @field_validator("*", mode="before")
    @classmethod
    def sanitize(cls, v):
        return cls._sanitize(v)

    @field_validator("*", mode="after")
    @classmethod
    def validate(cls, v):
        return cls._validate(v)

    @field_validator("permission_name", "role_name", mode="after", check_fields=False)
    @classmethod
    def to_lower_case(cls, v: str):
        return v.lower()

    model_config = {
        "extra": "forbid", # reject unknown fields
        "str_strip_whitespace": False, # we control trimming ourselves
    }
