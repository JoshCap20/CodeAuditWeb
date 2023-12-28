import subprocess

from .logger import get_logger

def execute_file(file_path: str) -> str:
    """
    Executes the code file specified in the request using the Python interpreter.

    Args:
        request (CodeRequest): The code request object containing the code file path.

    Returns:
        str: The output of the executed code.

    Raises:
        Exception: If an error occurs during execution.
    """
    logger = get_logger(__name__)
    try:
        return subprocess.run(["python", file_path], check=True, capture_output=True).stdout.decode("utf-8")
    except Exception as e:
        logger.error(f"Error occurred during execution: {e}")
        return f"Error occurred during execution: {e}"