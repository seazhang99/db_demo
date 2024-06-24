from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
import os
import ollama

from intent_helper import topic_intent
from db import db_query
from config import SCHEMA_FILE_PATH

class ChatBot:
    def __init__(self, host:str = 'localhost'):
        """
        Sample parameters for options could be as below:
          "options": {
                "num_keep": 5,
                "seed": 42,
                "num_predict": 100,
                "top_k": 20,
                "top_p": 0.9,
                "tfs_z": 0.5,
                "typical_p": 0.7,
                "repeat_last_n": 33,
                "temperature": 0.8,
                "repeat_penalty": 1.2,
                "presence_penalty": 1.5,
                "frequency_penalty": 1.0,
                "mirostat": 1,
                "mirostat_tau": 0.8,
                "mirostat_eta": 0.6,
                "penalize_newline": true,
                "stop": ["\n", "user:"],
                "numa": false,
                "num_ctx": 1024,
                "num_batch": 2,
                "num_gpu": 1,
                "main_gpu": 0,
                "low_vram": false,
                "f16_kv": true,
                "vocab_only": false,
                "use_mmap": true,
                "use_mlock": false,
                "num_thread": 8
            }
            I only use temperature and top_p here to ensure the minimum diversity.
        """
        self.host = host
        self.base_url = "http://%s:11434"%host
        #self.client = ollama.Client(host = self.host)


    def chat(self, question):
        intent = topic_intent(question=question)
        if intent['topic'] == 'General':
            return self.general_chat(question)
        else:
            return self.db_chat(intent=intent, question=question)

    def general_chat(self, question, model = "mistral", temperature=0.8, top_p=0.9):
        """
        Set temperature as 0.8 and top_p as 0.9 to increase the diversity of the result.
        """
        seed_prompt = """
        Answer the user question. 

        {question}

        Detect the language from the question.
        Response the answer in the same language detected from the question.
        """
        prompt = PromptTemplate.from_template(seed_prompt)
        llm = Ollama(model=model, base_url = self.base_url, temperature=temperature, top_p=top_p)
        chain = (
            prompt
            | llm
            | StrOutputParser()
        )
        return {"status": "Success", "type": "General", "msg": chain.invoke({"question": question})}
    
    def db_chat(self, intent, question, model="codellama", temperature=0, top_p=0, output_format="raw"):
        schema_columns = open(os.path.join(SCHEMA_FILE_PATH, intent['schema_file']), 'r').read()
        seed_prompt = """
        ### Instructions:
        Your task is to convert a question into a SQL query, given a database schema.

        ### Input:
        Generate a SQL query that answers the question `{question}`.
        This query will run on a database whose schema is represented in this string:
        {schema_columns}\n

        ### Important:
        Note to use format 'YYYYMMDD' of date.
        
        ### Response:
        Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
        ```sql
        """
        prompt = PromptTemplate.from_template(seed_prompt)
        llm = Ollama(model=model, base_url = self.base_url, temperature = temperature, top_p = top_p)
        sql_response = (
            prompt
            | llm.bind(stop=["[```]"])
            | StrOutputParser()
        )
        ret = sql_response.invoke({'question': question, 'schema_columns': schema_columns})
        sql = ret.split("```")[0].strip().split(";")[0] + ";"

        try:
            result = db_query(sql, output_format)
            messages = {"status": "Success", "sql": sql, "msg": ret, "data" : result}
        except Exception as e:
            msg = str(e)
            messages = {"status": "Error", "type": "DB", "sql": sql, "msg": msg}

        return messages
    
    def image_chat(self, question, images: list[str], temperature=0, top_p=0, model="llava"):
        """
        The images parameter can contain a list of image paths or a image byte
        """
        client = ollama.Client(host=self.host)
        options = {"temperature": temperature, "top_p": top_p}
        res = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "images": images
                }
            ],
            options=options
        )
        return {"status": "Success", "type": "image", "msg": res['message']['content']}

#question = "Provide me top 10 business partners in year 2015 and sales organization is 'APJ'."
#question = "Find all the transactions where GL Account is 'Travel' in year 2018."
#question = "List top 10 transaction customers in year 2018."
#question = "List top 10 transactioned products in year '2018'. The information should include product name, product category name and the amount of transactions."
#intent = topic_intent(question)
#if intent['topic'] == 'General':
#    print('General chat')
#else:
#    result = sql_agent.generate_execute_sql(create_llm(), question, intent['schema_file'])
#    print(result)
#question = "跟我说一下玫瑰战争吧."
#question = "List all employees in department 'Office of CEO'."
#question = "Show me the total transaction amount per profit center."
#question = "Convert the data in the image in csv format"
#images = ['./barcharts.png']
#bot = ChatBot()
#print(bot.image_chat(question=question, images=images))