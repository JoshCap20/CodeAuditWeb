import os
import tempfile
from pydantic import validator

from .base import Base, FileLink
from utils import execute_file

class CodeRequest(Base):
    """Request model for code analysis."""

    code: str
    code_file: FileLink | None = None
    options: list[str]
    iterations: int = 10

    @validator("iterations")
    def validate_iterations(cls, v: int):
        if v < 1:
            raise ValueError("Iterations must be greater than 0")
        return v

    @validator("options")
    def validate_options(cls, v: list[str]):
        if not v:
            raise ValueError("Options cannot be empty")
        return v

    def generate_code_file(self) -> None:
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False
        ) as temp_file:
            temp_file.write(self.code)
            self.code_file = FileLink.from_path(temp_file.name)

    def delete_code_file(self) -> None:
        if self.code_file:
            os.remove(self.code_file.link)
            self.code_file = None

    def get_code_file(self) -> str:
        if not self.code_file:
            raise ValueError("Code file not set")
        return self.code_file.link

    def execute(self) -> str:
        return execute_file(self.get_code_file())