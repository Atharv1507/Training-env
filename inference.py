import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME")

# Initialize OpenAI client strictly using the required variables
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)
ENV_URL = "http://localhost:7860"

def run_baseline():

    tasks_response = requests.get(f"{ENV_URL}/tasks")
    tasks = tasks_response.json()
    
    overall_scores = []

    for task in tasks:
        task_id = task['id']
        print(f"\n--- Running Task {task_id}: {task['description']} ---")
        

        obs_data = requests.post(f"{ENV_URL}/reset?task_id={task_id}").json()
        code = obs_data['code_snippets']
        

        prompt = f"System: You are a  software engineer. Respond with context to the code.Task: {task['description']}\n\nCode:\n{code}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],max_tokens=100,
        )
        
        review_comment = response.choices[0].message.content
        print(f"Agent Review: {review_comment}...\n") 

        step_response = requests.post(
            f"{ENV_URL}/step", 
            json={"comment": review_comment}
        ).json()
        
        reward = step_response['reward']
        print(f"Result: Score = {reward['score']}, Feedback = {reward['feedback']}")
        overall_scores.append(reward['score'])

    avg_score = sum(overall_scores) / len(overall_scores)
    print(f"\n======================\nBaseline Average Score: {avg_score:.2f}\n======================")

if __name__ == "__main__":
    run_baseline()