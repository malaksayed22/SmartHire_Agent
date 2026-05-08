from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []


def chat_with_bot(job_description: str, question: str, keep_history: bool = True) -> str:
    system_prompt = f"""
You are a professional and friendly HR assistant for SmartHire.
Your role is to help job candidates understand the position they are applying for.

STRICT RULES:
1. ONLY answer questions directly related to this job posting.
2. If asked anything unrelated, say: "I can only answer questions about this specific job."
3. If information is not in the job description, say: "This detail was not included in the job posting. I recommend contacting HR directly."
4. Never make up salary, benefits, or requirements that are not stated.
5. Keep answers short, clear, and professional — max 3 sentences.
6. Always be warm, encouraging, and professional in tone.
7. If a candidate seems frustrated, acknowledge their concern before answering.
8. If a candidate greets you, greet them back warmly before answering.
9. Always end your response with an offer to help further.

JOB DESCRIPTION:
{job_description}

Remember: You represent SmartHire professionally. Every response reflects our brand.
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
        temperature=0.4
    )

    answer = response.choices[0].message.content.strip()

    if keep_history:
        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

    return answer


def reset_conversation():
    """Clear conversation history for a new session."""
    global conversation_history
    conversation_history = []


if __name__ == "__main__":
    print("Chatbot ready")