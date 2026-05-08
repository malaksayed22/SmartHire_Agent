import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_reader import extract_text
from Scorer.scorer import score_resume
from Ranker.ranker import get_top_candidates
from Chatbot.chatbot import chat_with_bot

load_dotenv()


def think(step_description: str, memory: list) -> None:
    print(f"[THINK] {step_description}")
    memory.append({"step": "think", "content": step_description})


def act(tool_name: str, memory: list) -> None:
    print(f"[ACT] Calling {tool_name}...")
    memory.append({"step": "act", "tool": tool_name, "status": "running"})


def observe(observation: str, memory: list, success: bool = True) -> None:
    status = "success" if success else "failed"
    print(f"[OBSERVE] {observation}")
    memory.append({"step": "observe", "content": observation, "status": status})


def done(task: str, result: dict, memory: list) -> dict:
    print(f"[DONE] Task '{task}' completed successfully!")
    memory.append({"step": "done", "task": task, "status": "complete"})
    return {
        "task": task,
        "result": result,
        "memory": memory,
        "agent": "SmartHire AI Recruitment Agent v2.0"
    }


def run_agent(task: str, **kwargs) -> dict:
    print(f"\n{'=' * 50}")
    print(f"[AGENT] SmartHire AI Agent — Task: {task.upper()}")
    print(f"{'=' * 50}")

    memory = [{"step": "init", "task": task, "agent": "SmartHire AI Agent v2.0"}]

    if task == "score":
        file_path = kwargs.get("file_path")
        job_description = kwargs.get("job_description")

        if not file_path:
            return {"error": "file_path is required for score task"}
        if not job_description:
            return {"error": "job_description is required for score task"}
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        think("Extract resume text before evaluating the candidate.", memory)

        act("resume_reader", memory)
        try:
            resume_text = extract_text(file_path)
            if not resume_text or len(resume_text.strip()) < 50:
                return {"error": "Resume appears to be empty or unreadable"}
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Failed to extract resume: {str(e)}", memory, success=False)
            return {"error": f"Could not read resume: {str(e)}"}

        observe(f"Successfully extracted {len(resume_text)} characters from resume.", memory)

        think("Evaluate resume against the job description using the scoring engine.", memory)

        act("scorer", memory)
        try:
            result = score_resume(resume_text, job_description)
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Scoring failed: {str(e)}", memory, success=False)
            return {"error": f"Could not score resume: {str(e)}"}

        observe(
            f"Scoring complete. Score: {result.get('score', 'N/A')}/100. "
            f"Experience level: {result.get('experience_level', 'N/A')}. "
            f"Recommended action: {result.get('recommended_action', 'N/A')}.",
            memory
        )

        return done("score", result, memory)

    elif task == "rank":
        candidates = kwargs.get("candidates")
        top_n = kwargs.get("top_n", 5)

        if not candidates:
            return {"error": "candidates list is required for rank task"}
        if not isinstance(candidates, list):
            return {"error": "candidates must be a list of dictionaries"}
        if len(candidates) == 0:
            return {"error": "candidates list is empty"}

        think(f"Rank {len(candidates)} candidates and return top {top_n}.", memory)

        act("ranker", memory)
        try:
            ranked = get_top_candidates(candidates, top_n=top_n)
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Ranking failed: {str(e)}", memory, success=False)
            return {"error": f"Could not rank candidates: {str(e)}"}

        top_candidate = ranked[0] if ranked else None
        observe(
            f"Successfully ranked {len(ranked)} candidates. "
            f"Top candidate: {top_candidate.get('name', 'N/A') if top_candidate else 'N/A'} "
            f"with score {top_candidate.get('score', 'N/A') if top_candidate else 'N/A'}/100.",
            memory
        )

        return done("rank", ranked, memory)

    elif task == "chat":
        job_description = kwargs.get("job_description")
        question = kwargs.get("question")

        if not job_description:
            return {"error": "job_description is required for chat task"}
        if not question:
            return {"error": "question is required for chat task"}
        if len(question.strip()) < 3:
            return {"error": "question is too short to process"}

        think(
            f"A candidate asked: '{question}'. Answer strictly from the job description.",
            memory
        )

        act("chatbot", memory)
        try:
            answer = chat_with_bot(job_description, question)
            memory[-1]["status"] = "success"
        except Exception as e:
            observe(f"Chatbot failed: {str(e)}", memory, success=False)
            return {"error": f"Could not generate answer: {str(e)}"}

        observe(f"Answer generated successfully. Response length: {len(answer)} characters.", memory)

        return done("chat", {"answer": answer}, memory)

    return {
        "error": f"Unknown task '{task}'. Valid tasks are: score, rank, chat",
        "valid_tasks": ["score", "rank", "chat"]
    }


if __name__ == "__main__":
    print("SmartHire AI Agent v2.0 ready")
    print("Valid tasks: score, rank, chat")