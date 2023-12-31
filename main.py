import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import config
from models import CodeRequest, Results
from measures import AnalysisHandler

from utils import get_logger

logger = get_logger(__name__)

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")


# Routes

## Pages 

@app.get("/")
def code_tester():
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
    
@app.get("/endpoint")
def endpoint_tester():
    """
    Endpoint for serving the endpoint file.

    Returns:
        FileResponse: The endpoint file response.

    Raises:
        HTTPException: If there is an error serving the endpoint file.
    """
    try:
        return FileResponse(config.ENDPOINT_FILE)
    except Exception as e:
        logger.error("Error while serving endpoint file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

## Helpful frontend APIs

@app.get("/languages", response_model=list[str])
def get_languages() -> list[str]:
    """
    Retrieve a list of languages available for analysis.

    Returns:
        list[str]: A list of language names.
    """
    return list(AnalysisHandler.languages.keys())

@app.get("/strategies", response_model=list[str])
def get_strategies(language: str) -> list[str]:
    """
    Retrieve a list of strategies available in the PerformanceAnalyzer.

    Returns:
        list[str]: A list of strategy names.
    """
    analyzer = AnalysisHandler.languages.get(language)
    if analyzer is None:
        raise HTTPException(status_code=404, detail=f"Language '{language}' not supported.")

    return list(analyzer.strategies.keys())

## the magic

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
        return AnalysisHandler.measure(request)
    # TODO: Improve error handling
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
