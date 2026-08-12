from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    NovaHub Base Schema

    Barcha Pydantic schemalar uchun asosiy klass.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
