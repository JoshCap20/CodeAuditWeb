from fastapi import FastAPI, HTTPException, staticfiles
from fastapi.responses import FileResponse

from models import CodeRequest, Results
from measures import PerformanceAnalyzer

from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()

# Static Files
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")


# Routes
@app.get("/")
def index():
    try:
        return FileResponse("./static/index/index.html")
    except Exception as e:
        logger.error("Error while serving static/index.html")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=Results)
async def process_code(request: CodeRequest) -> Results:
    try:
        return PerformanceAnalyzer.measure(request)
    # TODO: Improve error handling
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
