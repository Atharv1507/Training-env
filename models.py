from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    code_snippets:str
    task_description: str
    review_history:List[str]=[]

class Action(BaseModel):
    comment:str

class Reward(BaseModel):
    score:float
    feedback:str

class StepResult(BaseModel):
    observation:Observation
    reward:Reward
    done: bool

class StateResult(BaseModel):
    task_id:Optional[int]=None
    step_count:int
    done:bool
    review_history:List[str]=[]