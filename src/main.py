from fastapi import FastAPI
from Solver.puzzle import Puzzle , Bridge
from Solver.algorithms import solve_backtracking, geneticSolver, memeticSolver
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

@app.post("/solve")
def solve(request: dict):
    puzzle = Puzzle(rows=request["rows"], columns=request["cols"], islands=request["islands"])
    algorithm = request.get("algorithm")
    solution = None
    match algorithm:
        case "backtracking":
            solution = solve_backtracking(puzzle)
        case "genetic":
            solution = geneticSolver(puzzle, request["bridges"])
        case "memetic":
            solution = memeticSolver(puzzle, request["bridges"])
        case _:
            return {"error": "Invalid algorithm specified."}
    if solution is None:
        return {"error": "No solution found."}

    return solution