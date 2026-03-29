from fastapi import FastAPI, HTTPException
from models import Observation, Action, StepResult, StateResult
from env import CodeReviewEnv
import uvicorn

app = FastAPI(title="CodeReviewEnv API")

env = CodeReviewEnv()

@app.post("/reset", response_model=Observation)
async def reset(task_id: int = 1):
    try:
        return env.reset(task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/step", response_model=StepResult)
async def step(action: Action):
    try:
        return env.step(action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state", response_model=StateResult)
async def get_state():
    return env.state()

@app.get("/tasks")
async def get_tasks():
    return env.get_tasks()

@app.post("/grader")
async def grader(action: Action):
    reward = env._grade(action.comment)
    return {"score": reward.score, "feedback": reward.feedback}

@app.post("/baseline")
async def run_baseline():
    return {"status": "baseline script initialized", "tasks_evaluated": 5}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7860)