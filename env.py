from models import *

class CodeReviewEnv:
    TASKS = [
        {
            "id": 1,
            "description": "Review this JavaScript code for security issues",
            "code": """const express = require('express');
const app = express();

const STRIPE_SECRET_KEY = "sk_live_51abc123xyz789";
const PORT = 3000;

app.get('/charge', (req, res) => {
    res.send(`Processing with key: ${STRIPE_SECRET_KEY}`);
});

app.listen(PORT);"""
        },
        {
            "id": 2,
            "description": "Review this React code for architectural issues",
            "code": """function App() {
    const username = "john_doe";
    return <Dashboard username={username} />;
}
function Dashboard({ username }) {
    return <Sidebar username={username} />;
}
function Sidebar({ username }) {
    return <UserCard username={username} />;
}
function UserCard({ username }) {
    return <div>{username}</div>;
}"""
        },
        {
            "id": 3,
            "description": "Review this code thoroughly for all issues",
            "code": """const API_KEY = "AIzaSyB1234567890abcdef";

function App() {
    const userId = "user_42";
    return <Layout userId={userId} apiKey={API_KEY} />;
}
function Layout({ userId, apiKey }) {
    return <Content userId={userId} apiKey={apiKey} />;
}
function Content({ userId, apiKey }) {
    return <Profile userId={userId} apiKey={apiKey} />;
}"""
        }
    ]

    def __init__(self):
        self.current_task = None
        self.step_count = 0
        self.review_history = []
        self.done= False
        self.max_steps=3

    def reset(self , task_id:int  =1) -> Observation:
        for t in self.TASKS:
            if t['id']==  task_id:
                self.current_task = t
                break
        self.step_count = 0
        self.review_history = []
        self.done = False
        return Observation(
            code_snippets=self.current_task['code'],
            task_description=self.current_task['description'],
            review_history=[]
        )
    
    def step(self, action: Action) -> StepResult:
        if self.done:
            raise ValueError("Episode is done. Please call reset() first.")
        self.step_count += 1
        self.review_history.append(action.comment)
        reward=self._grade(action.comment)

        if self.step_count >= self.max_steps or reward.score >= 1.0:
            self.done = True
        obs=Observation(
            code_snippets=self.current_task['code'],
            task_description=self.current_task['description'],
            review_history=self.review_history.copy()
        )
        return StepResult(
            observation=obs,
            reward=reward,
            done=self.done
        )
    
    def state(self) -> StateResult:
        return StateResult(
            task_id=self.current_task['id'] if self.current_task else None,
            step_count=self.step_count,
            done=self.done,
            review_history=self.review_history.copy()
        )
    
    def get_tasks(self) -> list:
        return [{"id": t["id"],
                  "description": t["description"]}
                    for t in self.TASKS]
    
    def _grade(self, comment:str) -> Reward:
        comment_lower = comment.lower()
        task_id = self.current_task['id']
        if task_id == 1:
            return self._grade_task1(comment_lower)
        elif task_id == 2:
            return self._grade_task2(comment_lower)
        elif task_id == 3:
            return self._grade_task3(comment_lower)
        
    def _grade_task1(self, comment:str) -> Reward:
        score = 0.0

        if any(k in comment for k in ["secret", "key", "api key", "hardcoded", "sk_live"]):
            score += 0.3
        if any(k in comment for k in ["stripe", "sk_live", "line 4"]):
            score += 0.3
        if any(k in comment for k in [".env", "dotenv", "enviornment variable"]):
            score += 0.4
        
        return Reward(score=min(score,1.0), feedback=f"Security score: {score:.1f}")

    def _grade_task2(self, comment: str) -> Reward:
        score = 0.0
        if any(k in comment for k in ["prop drilling", "props", "passing"]):
            score += 0.4
        if any(k in comment for k in ["username", "chain", "levels"]):
            score += 0.3
        if any(k in comment for k in ["context", "redux", "usecontext", "state management"]):
            score += 0.3
        return Reward(score=min(score, 1.0), feedback=f"Architecture score: {score:.1f}")

    def _grade_task3(self, comment: str) -> Reward:
        score = 0.0
        if any(k in comment for k in ["api key", "hardcoded", "secret", "api_key"]):
            score += 0.5
        if any(k in comment for k in ["prop drilling", "props", "context", "userid"]):
            score += 0.5
        return Reward(score=min(score, 1.0), feedback=f"Full review score: {score:.1f}")