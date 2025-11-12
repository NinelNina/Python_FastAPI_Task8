from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import List
from datetime import datetime, date
import re


class AppealBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    last_name: str
    first_name: str
    birth_date: date
    phone: str
    email: EmailStr

    @field_validator('last_name', 'first_name')
    def validate_cyrillic_name(cls, v: str) -> str:
        if not re.match(r'^[А-ЯЁ][а-яё]*$', v):
            raise ValueError('Должно содержать только кириллицу и начинаться с заглавной буквы')
        return v

    @field_validator('phone')
    def validate_phone(cls, v: str) -> str:
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^(\+7|7|8)?[489]\d{9,10}$', cleaned_phone):
            raise ValueError('Неверный формат номера телефона. Используйте российский формат номера')
        return v


class ProblemInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    problem_type: str = Field(..., description="Тип проблемы")
    detection_datetime: datetime

    @field_validator('problem_type')
    def validate_problem_type(cls, v: str) -> str:
        allowed_problems = [
            "нет доступа к сети",
            "не работает телефон",
            "не приходят письма"
        ]
        if v not in allowed_problems:
            raise ValueError(f'Тип проблемы должен быть одним из: {", ".join(allowed_problems)}')
        return v


class AppealCreate(AppealBase):
    problem: ProblemInfo


class AppealCreateMultiple(AppealBase):
    problems: List[ProblemInfo] = Field(..., min_items=1, description="Список проблем")

    @field_validator('problems')
    def validate_unique_problems(cls, v: List[ProblemInfo]) -> List[ProblemInfo]:
        problem_types = [problem.problem_type for problem in v]
        if len(problem_types) != len(set(problem_types)):
            raise ValueError('Причины обращения не должны повторяться')
        return v


class AppealResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str
    appeal_data: dict
    created_at: datetime
