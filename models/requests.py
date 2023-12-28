from .base import Base

from pydantic import validator


class Code(Base):
    """Model for representing code as a string."""

    code_str: str

    @validator("code_str")
    def validate_code(cls, v: str):
        if not v:
            raise ValueError("Code cannot be empty")
        return v

    def __str__(self):
        return self.code_str


class CodeRequest(Base):
    """Request model for code analysis."""

    code: Code
    options: list[str]
    iterations: int = 10
