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
    * Ollama tested with Microsoft Phi 3/3.5 model, performs better than Gemma
    * You can pull and test any model from [Ollama library](https://ollama.com/library)
    * with your own OPENAI_API_KEY you can choose gpt-3.5/gpt-4
- Docker and docker-compose for containerization
- Streamlit web application for conversational interface
- PostgreSQL to store asked questions, answers, evaluation (relevance) and user feedback
- Grafana to monitor performance

## 🚀 Instructions to reproduce

- [Setup environment](#hammer_and_wrench-setup-environment)
- [Start the app](#arrow_forward-start-the-app)
- [Interact with the app](#speech_balloon-interact-with-the-app)
- [Monitoring](#bar_chart-monitoring)
- [Best practices](#best-practices)

### :hammer_and_wrench: Setup environment

1. Fork this repo on GitHub. Or use `git clone https://github.com/dmytrovoytko/llm-exam-assistant.git` command to clone it locally, then `cd llm-exam-assistant`.
2. Create GitHub CodeSpace from the repo, use 4-core - 16GB RAM machine type.
3. **Start CodeSpace**
4. As app works in docker containers, the only package needed to install locally is `dotenv` for setting up Grafana dashboard - run `pip install dotenv` to install required package.
5. Go to the app directory `cd exam_assistant`
6. If you want to play with/develop the project locally, you can run `pip install -r requirements.txt` (project tested on python 3.11/3.12).
6. If you want to use gpt-3.5/gpt-4 API you need to correct OPENAI_API_KEY in `.env` file. 

### :arrow_forward: Start the app

1. Run `bash deploy.sh` to start all containers - elasticsearch, ollama, postgres, streamlit, grafana. It takes at least couple of minutes to download/build corresponding images, then get services ready to serve. When new log messages stop appering, press enter to return to command line. 
2. Run `bash init_db.sh` to create PostgreSQL tables.
![init_db](/screenshots/init_db.png)

3. Run `bash init_es.sh` to ingest and index question database.
![init_es](/screenshots/init_es.png)

4. Run `bash ollama_pull.sh` to pull phi3/phi3.5 Ollama models.
![Ollama pull](/screenshots/ollama_pulled.png)

5. Finally, open streamlit app: switch to ports tab and click on link with port 8501 (🌐 icon).

![Ports streamlit open](/screenshots/streamlit-open.png)

### :speech_balloon: Interact with the app

1. Set query parameters - choose exam, model, enter question.
2. Press 'Ask' button, wait for response. For Ollama Phi3 in CodeSpace response time is around a minute.
![streamlit ask](/screenshots/streamlit-00.png)

3. Check relevance evaluated by LLM.
![streamlit check](/screenshots/streamlit-02.png)

4. Give your feedback by pressing 👍 or 👎

5. You can switch to wide mode in streamlit settings (upper right corner)
![streamlit check](/screenshots/streamlit-03.png)

### :bar_chart: Monitoring

You can monitor app performance in Grafana dashboard

1. Create dashboard by running `bash init_gr.sh`.
2. As with streamlit switch to ports tab and click on link with port 3000 (🌐 icon).
- Login: "admin"
- Password: "admin"
3. Click 'Dashboards' and choose 'Exam Assistant'

![Grafana dasboard](/screenshots/grafana.png)

### Best practices
 * [x] Hybrid search: combining both text and vector search (Elastic search, encoding)
 * [x] User query rewriting (adding context)

## Next steps

I plan to add more questions to knowledge database and test more models.

Stay tuned!

## Support

🙏 Thank you for your attention and time!

- If you experience any issue while following this instruction (or something left unclear), please add it to [Issues](/issues), I'll be glad to help/fix. And your feedback, questions & suggestions are welcome as well!
- Feel free to fork and submit pull requests.

If you find this project helpful, please ⭐️star⭐️ my repo 
https://github.com/dmytrovoytko/llm-exam-assistant to help other people discover it 🙏

Made with ❤️ in Ukraine 🇺🇦 Dmytro Voytko
