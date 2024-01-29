import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse_resume(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def get_gemini_repsonse_question(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

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

## streamlit app
# st.title("Smart ATS")
# st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response_R=get_gemini_repsonse_resume(input_prompt.format(text=text, jd=jd))
        response_Q=get_gemini_repsonse_resume(input_question_prompt.format(text=text, jd=jd))
        st.write("Resume Analysis")
        st.json(response_R)
        st.write("Question")
        st.json(response_Q)
        