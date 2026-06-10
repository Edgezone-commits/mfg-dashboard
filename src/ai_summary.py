from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_summary(kpis, rush_orders, overdue_jobs):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are a manufacturing operations assistant.
    Write a short, clear morning briefing for the operations manager based on this data:

    - Total Jobs: {kpis['total']}
    - Completed Jobs: {kpis['completed']}
    - Rush Orders: {kpis['rush']}
    - Overdue Jobs: {kpis['overdue']}
    - Average Build Time: {kpis['avg_hours']} hours

    Rush Orders Pending:
    {rush_orders[['job_id','customer_name','product','due_date']].to_string()}

    Overdue Jobs:
    {overdue_jobs[['job_id','customer_name','due_date']].to_string() if len(overdue_jobs) > 0 else 'None'}

    Write 3-4 sentences. Be direct. Flag the most urgent issues first.
    End with one recommended action for today.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text