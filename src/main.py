from fastapi import FastAPI

app = FastAPI(
    title="Bridges Puzzle Solver",
    description="An AI solver for Hashiwokakero puzzles.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Bridges Puzzle Solver API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

