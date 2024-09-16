# LLM project Exam Assistant

Pet project / Capstone project for DataTalks.Club LLM ZoomCamp`24: 

RAG application based on exam preparation questions for Azure and Google Cloud certification exams.

![LLM project Exam Assistant](/screenshots/llm-exam-assistant.png)

Project can be tested and deployed in cloud virtual machine (AWS, Azure, GCP), **GitHub CodeSpaces** (the easiest option, and free), or even locally with/without GPU! Works with Ollama and ChatGPT.

For GitHub CodeSpace option you don't need to use anything extra at all - just your favorite web browser + GitHub account is totally enough.

## Problem statement

At some point of IT career many of us think about getting certified - to have better chances to be hired, or get better position/salary, or just to confirm expertise.
And then we face those exam guides, certification preparation books, exam questions and mock tests. Many things we need to remember. But crumming doesn't work well, especially with hundreds of terms, services and tools - thanks to cloud providers - they made a lot for us.

How can we increase chances to remember material well to pass exam? Understand it better, discover more connections. For this we need to have opportunity to ask questions - about things that are not clear yet. 
But you cannot ask the book or exam guide! Let's be honest, googling exam related questions is not efficient (sorry Goggle) and can be quite distracting (wikipedia-effect - attention lost). 
Thanks to technology, we have all those LLMs and "chatgpt"s - now we can ask chatbots. Still, they can hallucinate, are not trained well for specific topics yet.

And here is RAG comes to help! RAG is Retrieval Augmented Generation - the process of optimizing the output of a large language model (LLM). It references an authoritative knowledge base outside of its training data sources before generating a response. So instead of asking LLM about exam topics "from scratch", you first get context from prepared knowledge base (exam flashcards, question bank) and then get better focused answers. This is what I decided to do in my project.

Just imagine, you can 'talk to your data'!

## 🎯 Goals

This is my LLM project started during [LLM ZoomCamp](https://github.com/DataTalksClub/llm-zoomcamp)'24.

LLM Exam Assistant is a RAG application designed to assist users with their [data/cloud] exam preparation. It makes possible conversational interaction - via chatbot-like interface to easily get information without looking through guides or websites.

Actually, I strive to make inner logic universal enough, so knowledge base can be on any topic, data/cloud related exams is what I have been working this year.

Thanks to LLM ZoomCamp for the reason to approach exams and learning with many new tools! 

## Dataset

I assembled question banks for 2 exams: Azure DP 900 and Google Cloud Professional Data Engineer.
Azure flashcards I extracted from shared Anki deck. Google PDE flashcards I collected from official study guide. Adding more data is a matter of time.

CSV files are located in [data](/data) directory. 
**Structure**: id, question, answer, exam, section.

Section helps to focus on specific parts of exam.

## :toolbox: Tech stack

- Elastic search to index question bank
- OpenAI-compatible API, that supports working with Ollama locally, even without GPU
- Ollama tested with Microsoft Phi 3/3.5 model
- Docker and docker-compose for containerization
- Streamlit web application for conversational interface
- PostgreSQL to store asked questions, answers, evaluation (relevance) and user feedback
- Grafana to monitor performance

