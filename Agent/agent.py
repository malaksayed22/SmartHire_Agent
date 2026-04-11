from groq import Groq
from dotenv import load_dotenv
import os
import json

from resume_reader import extract_text
from scorer import score_resume
from ranker import rank_candidates, get_top_candidates
from chatbot import chat_with_bot, reset_conversation

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_agent(task: str, **kwargs) -> dict:
    """
    Main agent function decides what to do based on the task
    
    Tasks:
    -score  -> extract text from resume + score it
    -rank   -> rank a list of candidates
    -chat   -> answer a question about a job
    """
    
    print(f"\n[AGENT] Task received: {task}")
    memory = []

    # Task1: score a resume
    if task == "score":
        file_path      = kwargs.get("file_path")
        job_description = kwargs.get("job_description")

        if not file_path or not job_description:
            return {"error": "file_path and job_description are required"}

        # think
        print("[THINK] I need to extract text from the resume first")
        memory.append({"step": "think", "content": "extract resume text"})

        # act: call resume reader
        print("[ACT] Calling resume_reader...")
        try:
            resume_text = extract_text(file_path)
            memory.append({"step": "act", "tool": "resume_reader", "status": "success"})
        except Exception as e:
            return {"error": f"Could not read resume: {str(e)}"}

        # OBSERVE
        print(f"[OBSERVE] Got {len(resume_text)} characters of text")
        memory.append({"step": "observe", "content": f"{len(resume_text)} chars extracted"})

        # THINK again
        print("[THINK] Now I need to score the resume against the job description")
        memory.append({"step": "think", "content": "score resume vs job description"})

        # ACT: call scorer
        print("[ACT] Calling scorer...")
        try:
            result = score_resume(resume_text, job_description)
            memory.append({"step": "act", "tool": "scorer", "status": "success"})
        except Exception as e:
            return {"error": f"Could not score resume: {str(e)}"}

        # observe
        print(f"[OBSERVE] Score received: {result['score']}/100")
        memory.append({"step": "observe", "content": f"score = {result['score']}"})

        # done
        print("[DONE] Task complete!")
        return {
            "task": "score",
            "result": result,
            "memory": memory
        }

    # task2: rank candidates 
    elif task == "rank":
        candidates = kwargs.get("candidates")
        top_n      = kwargs.get("top_n", 5)

        if not candidates:
            return {"error": "candidates list is required"}

        # think
        print("[THINK] I need to rank these candidates by score")
        memory.append({"step": "think", "content": "rank candidates"})

        # act: call ranker
        print("[ACT] Calling ranker...")
        ranked = get_top_candidates(candidates, top_n=top_n)
        memory.append({"step": "act", "tool": "ranker", "status": "success"})

        # observe
        print(f"[OBSERVE] Ranked {len(ranked)} candidates")
        memory.append({"step": "observe", "content": f"{len(ranked)} candidates ranked"})

        # done
        print("[DONE] Task complete!")
        return {
            "task": "rank",
            "result": ranked,
            "memory": memory
        }

    #task3:chat
    elif task == "chat":
        job_description = kwargs.get("job_description")
        question        = kwargs.get("question")

        if not job_description or not question:
            return {"error": "job_description and question are required"}

        # think
        print("[THINK] I need to answer a candidate question about the job")
        memory.append({"step": "think", "content": "answer job question"})

        #act: call chatbot
        print("[ACT] Calling chatbot...")
        answer = chat_with_bot(job_description, question)
        memory.append({"step": "act", "tool": "chatbot", "status": "success"})

        #observe
        print(f"[OBSERVE] Answer generated")
        memory.append({"step": "observe", "content": "answer ready"})

        #done
        print("[DONE] Task complete!")
        return {
            "task": "chat",
            "result": {"answer": answer},
            "memory": memory
        }

    else:
        return {"error": f"Unknown task: {task}"}


if __name__ == "__main__":
    print("Agent ready")
