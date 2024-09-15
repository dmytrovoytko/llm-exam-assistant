import json

from time import time

try:
    from openai import OpenAI
    client = OpenAI(
        base_url='http://localhost:11434/v1/',
        api_key='ollama',
    )
except:
    client = {}

MODEL_NAME = "phi3.5" # "phi3" # gpt-4o-mini

import ingest
# index = ingest.load_index()

def search(query, index):
    boost = {
        # "question": 1.5,
        # "answer": 2,
        # "exam": 0.5,
        # "section": 0.5,
    }

    results = index.search(
        query=query, filter_dict={}, boost_dict=boost, num_results=3, threshold=0.4
    )

    return results


prompt_template = """
You're an exam preparation coach. Answer the QUESTION based on the CONTEXT from our questions database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()


entry_template = """
hint: {question} - {answer}
""".strip()
# exam: {exam}
# section: {section}


def build_prompt(query, search_results):
    context = ""

    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt, model=MODEL_NAME):
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    token_stats = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return answer, token_stats


evaluation_prompt_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


def evaluate_relevance(question, answer):
    prompt = evaluation_prompt_template.format(question=question, answer=answer)
    evaluation, tokens = llm(prompt, model=MODEL_NAME)
    # print('evaluate_relevance', prompt, evaluation)
    if evaluation.startswith('```json'):
        # remove extra formatting ```json ... ```
        evaluation = evaluation[7:-3].strip()
        # print('evaluate_relevance', evaluation)

    try:
        json_eval = json.loads(evaluation)
        return json_eval, tokens
    except json.JSONDecodeError:
        print('!! evaluation parsing failed:', evaluation)
        if find(evaluation, "RELEVANT")>=0:
            result = {"Relevance": "RELEVANT", "Explanation": evaluation}
        elif find(evaluation, "PARTLY_RELEVANT")>=0:
            result = {"Relevance": "PARTLY_RELEVANT", "Explanation": evaluation}
        elif find(evaluation, "NON_RELEVANT")>=0:
            result = {"Relevance": "NON_RELEVANT", "Explanation": evaluation}
        else:
            result = {"Relevance": "UNKNOWN", "Explanation": f"Failed to parse evaluation. {evaluation}"}
        return result, tokens


def calculate_openai_cost(model, tokens):
    openai_cost = 0

    if model == "gpt-4o-mini":
        openai_cost = (
            tokens["prompt_tokens"] * 0.00015 + tokens["completion_tokens"] * 0.0006
        ) / 1000
    elif model in ["phi3", "phi3.5"]:
        pass # free ollama model
    else:
        print("Model not recognized. OpenAI cost calculation failed.")

    return openai_cost


def rag(query, index, model=MODEL_NAME):
    t0 = time()

    search_results = search(query, index)
    prompt = build_prompt(query, search_results)

    return search_results, prompt

    answer, token_stats = llm(prompt, model=model)

    relevance, rel_token_stats = evaluate_relevance(query, answer)
    took = time() - t0

    openai_cost_rag = calculate_openai_cost(model, token_stats)
    openai_cost_eval = calculate_openai_cost(model, rel_token_stats)

    openai_cost = openai_cost_rag + openai_cost_eval

    answer_data = {
        "answer": answer,
        "model_used": model,
        "response_time": took,
        "relevance": relevance.get("Relevance", "UNKNOWN"),
        "relevance_explanation": relevance.get(
            "Explanation", "Failed to parse evaluation"
        ),
        "prompt_tokens": token_stats["prompt_tokens"],
        "completion_tokens": token_stats["completion_tokens"],
        "total_tokens": token_stats["total_tokens"],
        "eval_prompt_tokens": rel_token_stats["prompt_tokens"],
        "eval_completion_tokens": rel_token_stats["completion_tokens"],
        "eval_total_tokens": rel_token_stats["total_tokens"],
        "openai_cost": openai_cost,
    }

    return answer_data

#############

if __name__ == '__main__':

    t0 = time()
    index = ingest.load_index()
    took = time() - t0
    print(f'Indexing finished in {took:05.3f} sec')

    question = 'What is the Data Analyst role responsible for?'
    answer = rag(question, index, model=MODEL_NAME)
    print(f'\nQ: {question}\n A: {answer}')

    question = 'What is Data processing?'
    answer = rag(question, index, model=MODEL_NAME)
    print(f'\nQ: {question}\n A: {answer}')

    question = 'What storage types does Databricks use?'
    answer = rag(question, index, model=MODEL_NAME)
        # What types of storage can Databricks process data in?
        # "Azure Blob storage, Azure Data Lake Store, Hadoop storage, flat files, SQL Databases, 
        #  and data warehouses, and Azure services such as Cosmos DB."    
    # print(f'\nQ: {question}\n A: {answer["answer"]}', f'took {answer["response_time"]} sec')
    print(f'\nQ: {question}\n A: {answer}')


