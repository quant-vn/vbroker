from pydantic import BaseModel as BM, ConfigDict, Field, AliasChoices  # noqa: F401


class BaseModel(BM):
    model_config: ConfigDict = ConfigDict(
        use_enum_values=True,
        validate_return=True
    )
