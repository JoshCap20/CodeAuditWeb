import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import config
from models import CodeRequest, Results
from measures import PerformanceAnalyzer

from utils import get_logger

logger = get_logger(__name__)

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")


# Routes
@app.get("/")
def index():
    """
    Endpoint for serving the index file.

    Returns:
        FileResponse: The index file response.

    Raises:
        HTTPException: If there is an error serving the index file.
    """
    try:
        return FileResponse(config.INDEX_FILE)
    except Exception as e:
        logger.error("Error while serving index file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/strategies", response_model=list[str])
def get_strategies() -> list[str]:
    """
    Retrieve a list of strategies available in the PerformanceAnalyzer.

    Returns:
        list[str]: A list of strategy names.
    """
    return list(PerformanceAnalyzer.strategies.keys())


@app.post("/analyze", response_model=Results)
async def process_code(request: CodeRequest) -> Results:
    """
    Process the given code request with performance measures and return the results.

    Args:
        request (CodeRequest): The code request object containing the code to be analyzed.

    Returns:
        Results: The results of the code analysis.

    Raises:
        HTTPException: If there is an error during the code analysis.
    """
    try:
        return PerformanceAnalyzer.measure(request)
    # TODO: Improve error handling
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
