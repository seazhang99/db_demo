import os
import pandas as pd
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

from config import MINILM_EMBEDDING
from langchain.utils.math import cosine_similarity


general_chat = """You are a smart robot to chat with all general topic.
Any other topics don't match will put under your category.

Here is a question:
{query}"""

sales_chat = """You are a very smart analytics expert on sales data. \
You are great at answering questions about sales orders in a concise and easy to understand manner. \
You are going to read the data from database to find the perfect answers by question. \
The sales order data should include business partners, sales orders and the line items in the sales orders. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{query}"""

finance_chat = """You are a very smart analytics expert on financial data. \
You are great at answering questions about finance data in a concise and easy to understand manner. \
You are going to read the data from database to find the perfect answers by question. \
The finance data should include customers, GL account, profit center and products. \
The finance transaction is different to the sales order, which is linked to the end customer instead of business partners. \
Never mix the finance transaction with the sales orders. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{query}"""

hr_chat = """You are a very smart analytics expert on HR data. \
You are great at answering questions about HR data in a concise and easy to understand manner. \
You are going to read the data from database to find the perfect answers by question. \
The finance data should include employee information, e.g. head count, personal, postion, job, division, department, HR manager. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{query}"""


def topic_intent(question):
    routers = pd.DataFrame()
    routers['topic'] = ['General', 'Sales', 'FI', 'HR']
    routers['schema_file'] = ['', 'sales_schema.txt', 'finance_schema.txt', 'hr_schema.txt']
    routers['capabilities'] = [general_chat, sales_chat, finance_chat, hr_chat]
    prompt_embeddings = MINILM_EMBEDDING.embed_documents(routers['capabilities'].values)
    query_embedding = MINILM_EMBEDDING.embed_query(question)
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    print(similarity)
    most_similar = routers.iloc[similarity.argmax()]
    return most_similar    

def intent_fewshot(query):
    df = pd.read_csv(os.path.join('./data/few-shot', 'prompt_intent.csv'), sep="|")
    examples = []

    for _, row in df.iterrows():
        question, intent = row
        examples.append({"question": question, "intent":intent})

    #example_prompt = PromptTemplate(
    #    input_variables=["question", "intent"], template="Question: {question}\n{intent}"
    #)

    #print(prompt.invoke(input=question).to_string())
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        # This is the list of examples available to select from.
        examples,
        # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
        MINILM_EMBEDDING,
        # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
        Chroma,
        # This is the number of examples to produce.
        k=1,
    )

    # Select the most similar example to the input.
    #question = "Show me the total transaction amount."
    selected_examples = example_selector.select_examples({"question": query})
    return selected_examples

#questions = ["How many products we have?", "Pull me SO data of year 2018 with product name and total amount."]
#result = []
#for question in questions:
#    result.append({'question': question, 
#                   'topic_intent': topic_intent(question)['topic'], 
#                   'fewshot': intent_fewshot(question)[0]['intent']})

#print(result)