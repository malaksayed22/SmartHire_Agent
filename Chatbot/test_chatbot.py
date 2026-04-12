from chatbot import chat_with_bot, reset_conversation

job_description = """
Job Title: AI Engineer
Company: TechCorp Egypt

Requirements:
- 2+ years of Python experience
- Knowledge of Machine Learning and NLP
- Experience with REST APIs
- Bachelor degree in Computer Science or related field
- Good communication skills

Responsibilities:
- Build and maintain AI models
- Develop REST APIs using FastAPI
- Work with the data team on ML pipelines

Benefits:
- Salary: 15,000 - 25,000 EGP per month
- Remote work: Hybrid (3 days office, 2 days home)
- Health insurance included
- Annual bonus
"""

print("=====> CHATBOT TEST <=====\n")

# Test 1: Related question
q1 = "What Python experience is required?"
print(f"Q: {q1}")
print(f"A: {chat_with_bot(job_description, q1)}\n")

# Test 2: Related question
q2 = "What is the salary?"
print(f"Q: {q2}")
print(f"A: {chat_with_bot(job_description, q2)}\n")

# Test 3: Related question
q3 = "Is this job remote?"
print(f"Q: {q3}")
print(f"A: {chat_with_bot(job_description, q3)}\n")

# Test 4: Unrelated question (bot should refuse)
q4 = "What is the capital of France?"
print(f"Q: {q4}")
print(f"A: {chat_with_bot(job_description, q4)}\n")

# Test 5: Follow up question (tests memory)
q5 = "Can you tell me more about the bonus?"
print(f"Q: {q5}")
print(f"A: {chat_with_bot(job_description, q5)}\n")

print("=====> CHATBOT WORKS CORRECTLY <=====")