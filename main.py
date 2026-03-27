from fastapi import FastAPI, HTTPException
from models import Observation, Action, StepResult, StateResult
from env import CodeReviewEnv
import uvicorn

app = FastAPI(title="CodeReviewEnv API")

# Initialize the environment
# Note: In a production multi-user scenario, you'd track sessions.
# For the hackathon/HF Space, a global instance is usually acceptable.
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
    # The OpenEnv spec often uses the internal _grade logic
    # to provide a final score for a specific action.
    reward = env._grade(action.comment)
    return {"score": reward.score, "feedback": reward.feedback}

@app.post("/baseline")
async def run_baseline():
    # This will eventually call your baseline script logic
    # For now, we return a placeholder to pass the initial ping
    return {"status": "baseline script initialized", "tasks_evaluated": 3}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7860)