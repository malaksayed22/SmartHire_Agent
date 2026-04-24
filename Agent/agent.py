from groq import Groq
from dotenv import load_dotenv
import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_reader import extract_text
from Scorer.scorer import score_resume
from Ranker.ranker import rank_candidates, get_top_candidates
from Chatbot.chatbot import chat_with_bot, reset_conversation

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


AGENT_SYSTEM_PROMPT = """
You are SmartHire's AI Recruitment Agent — an expert intelligent system 
designed to assist HR teams in making fast,fair and accurate hiring decisions.

YOUR CAPABILITIES:
1. Resume Analysis    — Extract and understand resume content from PDF/DOCX files
2. Candidate Scoring  — Evaluate candidates against job requirements (score 0–100)
3. Candidate Ranking  — Sort and shortlist the best candidates automatically
4. Job Q&A Chatbot    — Answer candidate questions about specific job postings

YOUR CORE PRINCIPLES:
- Always be objective and fair in every evaluation
- Never make assumptions beyond what is in the resume or job description
- Always complete the full ReAct loop: Think → Act → Observe → Done
- If a step fails, report the error clearly and stop gracefully
- Every decision must be explainable and traceable through memory logs

REACT LOOP RULES:
- THINK  : Analyze the task and decide the next best action
- ACT    : Execute the chosen tool with precision
- OBSERVE: Carefully read and validate the tool result
- DONE   : Only return when the task is fully complete and verified

QUALITY STANDARDS:
- Resume scores must be based on real skills and experience — not resume length
- Rankings must always be sorted correctly from highest to lowest score
- Chatbot answers must only use information from the job description
- All responses must be structured, clear, and professional
"""


def think(step_description: str, memory: list) -> None:
    """Log a THINK step"""
    print(f"[THINK] {step_description}")
    memory.append({"step": "think", "content": step_description})


def act(tool_name: str, memory: list) -> None:
    """Log an ACT step"""
    print(f"[ACT] Calling {tool_name}...")
    memory.append({"step": "act", "tool": tool_name, "status": "running"})


def observe(observation: str, memory: list, success: bool = True) -> None:
    """Log an OBSERVE step"""
    status = "success" if success else "failed"
    print(f"[OBSERVE] {observation}")
    memory.append({"step": "observe", "content": observation, "status": status})


def done(task: str, result: dict, memory: list) -> dict:
    """Log DONE and return final result"""
    print(f"[DONE] Task '{task}' completed successfully!")
    memory.append({"step": "done", "task": task, "status": "complete"})
    return {
        "task": task,
        "result": result,
        "memory": memory,
        "agent": "SmartHire AI Recruitment Agent v2.0"
    }


def run_agent(task: str, **kwargs) -> dict:
    """
    Main SmartHire agent — implements the upgraded ReAct loop.

    Available tasks:
    - 'score' : Extract text from resume + score against job description
    - 'rank'  : Rank a list of candidates by score
    - 'chat'  : Answer a candidate question about a specific job
    """

    print(f"\n{'='*50}")
    print(f"[AGENT] SmartHire AI Agent — Task: {task.upper()}")
    print(f"{'='*50}")

    memory = [{"step": "init", "task": task, "agent": "SmartHire AI Agent v2.0"}]

    # task1: score a resume
    if task == "score":
        file_path       = kwargs.get("file_path")
        job_description = kwargs.get("job_description")

        # validate inputs
        if not file_path:
            return {"error": "file_path is required for score task"}
        if not job_description:
            return {"error": "job_description is required for score task"}
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        # THINK1: extract resume text
        think("I need to extract the resume text before I can evaluate the candidate", memory)

        # ACT1: call resume reader
        act("resume_reader", memory)
        try:
            resume_text = extract_text(file_path)
            if not resume_text or len(resume_text.strip()) < 50:
                return {"error": "Resume appears to be empty or unreadable"}
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Failed to extract resume: {str(e)}", memory, success=False)
            return {"error": f"Could not read resume: {str(e)}"}

        # OBSERVE1: resume extracted
        observe(
            f"Successfully extracted {len(resume_text)} characters from resume. "
            f"Resume is ready for evaluation.",
            memory, success=True
        )

        # THINK2: score the resume
        think(
            "Resume text is ready. Now I need to evaluate it against the job description "
            "using the scoring engine to produce a fair and objective score.",
            memory
        )

        # ACT2: call scorer
        act("scorer", memory)
        try:
            result = score_resume(resume_text, job_description)
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Scoring failed: {str(e)}", memory, success=False)
            return {"error": f"Could not score resume: {str(e)}"}

        # OBSERVE2: score received
        observe(
            f"Scoring complete. Score: {result['score']}/100. "
            f"Experience level: {result.get('experience_level', 'N/A')}. "
            f"Recommended action: {result.get('recommended_action', 'N/A')}.",
            memory, success=True
        )

        # THINK3: validate and finalize
        think(
            f"Score of {result['score']}/100 received with "
            f"{len(result.get('strengths', []))} strengths and "
            f"{len(result.get('weaknesses', []))} weaknesses identified. "
            f"Result is complete and ready to return.",
            memory
        )

        return done("score", result, memory)

    # TASK2: RANK CANDIDATES
    elif task == "rank":
        candidates = kwargs.get("candidates")
        top_n      = kwargs.get("top_n", 5)

        # validate inputs
        if not candidates:
            return {"error": "candidates list is required for rank task"}
        if not isinstance(candidates, list):
            return {"error": "candidates must be a list of dictionaries"}
        if len(candidates) == 0:
            return {"error": "candidates list is empty"}

        # THINK1: understand ranking task
        think(
            f"I have {len(candidates)} candidates to rank. "
            f"I will sort them by score and return the top {top_n}.",
            memory
        )

        # ACT1: call ranker
        act("ranker", memory)
        try:
            ranked = get_top_candidates(candidates, top_n=top_n)
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Ranking failed: {str(e)}", memory, success=False)
            return {"error": f"Could not rank candidates: {str(e)}"}

        # OBSERVE1: ranking complete
        top_candidate = ranked[0] if ranked else None
        observe(
            f"Successfully ranked {len(ranked)} candidates. "
            f"Top candidate: {top_candidate['name'] if top_candidate else 'N/A'} "
            f"with score {top_candidate['score'] if top_candidate else 'N/A'}/100.",
            memory, success=True
        )

        # THINK2: validate results
        think(
            f"Ranking complete. Returning top {len(ranked)} candidates "
            f"sorted from highest to lowest score.",
            memory
        )

        return done("rank", ranked, memory)

    # TASK3: CHAT
    elif task == "chat":
        job_description = kwargs.get("job_description")
        question        = kwargs.get("question")

        # validate inputs
        if not job_description:
            return {"error": "job_description is required for chat task"}
        if not question:
            return {"error": "question is required for chat task"}
        if len(question.strip()) < 3:
            return {"error": "question is too short to process"}

        # THINK 1: understand the question
        think(
            f"A candidate asked: '{question}'. "
            f"I need to find the answer strictly within the job description "
            f"without making up any information.",
            memory
        )

        # ACT1: call chatbot
        act("chatbot", memory)
        try:
            answer = chat_with_bot(job_description, question)
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Chatbot failed: {str(e)}", memory, success=False)
            return {"error": f"Could not generate answer: {str(e)}"}

        # OBSERVE1: answer generated
        observe(
            f"Answer generated successfully. "
            f"Response length: {len(answer)} characters.",
            memory, success=True
        )

        # THINK 2: validate answer
        think(
            "Answer is ready. Returning professional response to the candidate.",
            memory
        )

        return done("chat", {"answer": answer}, memory)

    #unknown task 
    else:
        print(f"[ERROR] Unknown task: {task}")
        return {
            "error": f"Unknown task '{task}'. Valid tasks are: score, rank, chat",
            "valid_tasks": ["score", "rank", "chat"]
        }


if __name__ == "__main__":
    print("SmartHire AI Agent v1.0 ready")
    print("Valid tasks: score, rank, chat")