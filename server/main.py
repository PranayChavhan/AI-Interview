
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file.file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst, Web developer, and other job profiles also. 
our task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy. find out the key skills of candidate and give feedback regarding resume match with job profile.
Find out Grammar score, content socre and clarity score of candidate resume in percentage.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD_Match":"%","Grammar_score":"%","Content_score":"%","Clarity_score":"%","MissingKeywords":[], "candidate_skills":[],"General_feedback":""}}
"""

input_question_prompt = """
Given the provided resume and job description, generate a set of interview questions for a candidate applying for the role described. 
Include a mix of general questions to assess personality, experience-related inquiries,questions related to job description,technical questions related to skills of candidate and interview closing questions.
create 5 questions of each category.
resume:{text}
job description:{jd}

I want the response in one single string having the structure
{{"general_questions":[],"experience_related":[],"questions_on_job_description":[],"questions_on_skills":[],"interview_closing_questions":[]}}
"""


@app.post("/Resume_analyser/")
async def submit_resume(jd: str = Form(...), resume: UploadFile = File(...)):
    text = input_pdf_text(resume)
    R_response = get_gemini_response(input_prompt.format(text=text, jd=jd))
    Q_response = get_gemini_response(input_question_prompt.format(text=text, jd=jd))
    return {"resume_response": R_response,"questions_response":Q_response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8081)


