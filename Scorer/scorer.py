from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def score_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a senior HR recruiter and technical hiring specialist with 15 years of experience
in the AI and software engineering industry.

Your task is to evaluate a candidate's resume against a specific job description and
produce a detailed, fair, and structured assessment.

EVALUATION CRITERIA:
1. Technical Skills Match
2. Experience Level
3. Education
4. Projects & Achievements
5. Soft Skills & Communication

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

SCORING GUIDE:
- 90-100: Exceptional match — exceeds all requirements
- 75-89: Strong match — meets most requirements with minor gaps
- 60-74: Moderate match — meets some requirements, needs development
- 40-59: Weak match — significant gaps in key areas
- 0-39: Poor match — does not meet core requirements

INSTRUCTIONS:
- Be specific in strengths and weaknesses.
- Do NOT give a high score just because the resume is long.
- Do NOT penalize for missing optional requirements.
- Be honest and objective.
- strengths list must have minimum 3 points.
- weaknesses list must have minimum 2 points.
- Each strength and weakness must be one clear sentence.

Reply ONLY with this exact JSON format, no extra text, no markdown:
{{
  "score": <number between 0 and 100>,
  "strengths": [
    "specific strength 1 from resume",
    "specific strength 2 from resume",
    "specific strength 3 from resume"
  ],
  "weaknesses": [
    "specific weakness 1",
    "specific weakness 2"
  ],
  "experience_level": "Junior / Mid-level / Senior",
  "recommended_action": "Shortlist / Consider / Reject",
  "summary": "2-3 sentence summary of the candidate and their fit for this role"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result_text = response.choices[0].message.content.strip()

    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]
        result_text = result_text.strip()

    return json.loads(result_text)


if __name__ == "__main__":
    print("Scorer ready")