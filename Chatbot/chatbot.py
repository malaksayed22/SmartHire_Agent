from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

def chat_with_bot(job_description: str, question: str, keep_history: bool = True) -> str:
    
    system_prompt = f"""You are a helpful HR assistant for a company.
Your job is to answer candidate questions about the following job ONLY.
If someone asks anything not related to this job, politely say:
'I can only answer questions about this specific job posting.'

JOB DESCRIPTION:
{job_description}

Rules:
- Be friendly and professional
- Keep answers short and clear
- Never make up information not in the job description
- If info is not in the job description, say 'This information was not provided in the job posting'
"""

    if keep_history:
        conversation_history.append({
            "role": "user",
            "content": question
        })
        messages = [{"role": "system", "content": system_prompt}] + conversation_history
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.5
    )

    answer = response.choices[0].message.content.strip()

    if keep_history:
        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

    return answer


def reset_conversation():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []


if __name__ == "__main__":
    print("Chatbot ready")