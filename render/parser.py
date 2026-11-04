import json
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidatorFunctionWrapHandler,
    ValidationInfo,
    ValidationError,
)
from pydantic.fields import FieldInfo
from typing import Any, List, Optional


class ParsingError(Exception):
    ...


def _field_info(
    cls: type[BaseModel], info: ValidationInfo
) -> Optional[FieldInfo]:
    if info.field_name is None:
        return None
    return cls.model_fields.get(info.field_name)


class Parser:
    def __init__(self, file: str) -> None:
        try:
            with open(file) as f:
                self.info = Info(**json.load(f))
        except Exception as e:
            self.info = Info(
                level=[Level(width=20, height=20) for _ in range(10)]
            )
            print(f"Error while loding configuration file:\n{e}")


class Level(BaseModel):
    width: int = Field(le=35, ge=11, default=21)
    height: int = Field(le=24, ge=11, default=21)

    @field_validator("*", mode="wrap")
    @classmethod
    def fallback_all(
        cls,
        v: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,
    ) -> Any:
        try:
            return handler(v)
        except (ValueError, ValidationError):
            field_info = _field_info(cls, info)

            if field_info is None or field_info.is_required():
                raise

            return field_info.get_default(call_default_factory=True)


class Info(BaseModel):
    highscore_filename: str = Field(default="score/score.json")
    level: List[Level] = Field(min_length=10)
    lives: int = Field(le=10, ge=1, default=3)
    pacgum: int = Field(le=100, ge=1, default=42)
    points_per_pacgum: int = Field(ge=1, le=1000, default=10)
    points_per_super_pacgum: int = Field(ge=5, le=5000, default=50)
    points_per_ghost: int = Field(ge=1, le=10000, default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(ge=1, le=10, default=90)

    @field_validator("*", mode="wrap")
    @classmethod
    def fallback_all(
        cls,
        v: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,
    ) -> Any:
        try:
            return handler(v)
        except (ValueError, ValidationError):
            field_info = _field_info(cls, info)

            if field_info is None or field_info.is_required():
                raise

            return field_info.get_default(call_default_factory=True)
