from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def score_resume(resume_text: str, job_description: str) -> dict:
    
    prompt = f"""
You are an expert HR recruiter with 10 years of experience.
Analyze this resume against the job description and give a match score.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Reply ONLY with this exact JSON format, no extra text, no markdown:
{{
  "score": <number between 0 and 100>,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "summary": "one sentence summary of the candidate"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    result_text = response.choices[0].message.content.strip()
    
    # Clean response if it has markdown code blocks
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]
    
    result = json.loads(result_text)
    return result


if __name__ == "__main__":
    print("Scorer ready")
