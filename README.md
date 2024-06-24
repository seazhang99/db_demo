# Introduction
As the evolvement of AI, we can earn more benefits from it in our work. Generating SQL from natrual language is one of the most important benefits among AI capability.

We can find several fine tuned LLM models to do such work, for example, codellama by Meta, sql-coder by defog.ai. These models allow you to add the table definition in the prompt, then generate SQL according to the user query.

However, Text-to-SQL may have two teasers:
- From the correctness and complexity perspective, the generated SQL is not so accuracy. If we don’t do any adjustment, the SQL can’t even run when in a complex database schema environment. Some illusion fields could be added in the SQL, which don’t exist in the table definitions.
- The length of prompt has limitation, we can’t just simple paste all the column definitions into prompt if we have thousands of tables.  

In this implementation, I am trying to solve these two issues with following work arounds:
- Add a sample SQL in the schema text to ensure the correctness of the generated SQL.
- Detect the intent from user query, in order to add only the necessary tables into the prompt.

The implementation also includes:
- Execute the generated SQL on HANA Cloud to retrieve the data – verify the correctness of the SQL.
- Present the result on an Web page – be easy to test the implementation.

# How to run the demo?
There's a lot of manaul works need to do so that you can run this demo.

## Prepare LLM
Download Ollama from link [https://ollama.com](https://ollama.com/) and pull the necessary LLM models. They are:
- qwen
- llama3
- mistral
- llava
- codellava

## Pull embedding from Huggingface
Pull embedding from link [https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/main](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/main) and place it to the folder embedding/all-MiniLM-L6-v2.

## Prepare Python environment
Assume you use conda and name your enviroment name as LLM-DEMO.
```
#conda create --name LLM-DEMO python=3.11
#conda activate LLM-DEMO
#pip install -r requirements.txt
```
## Prepare HANA Cloud Data
Create an HANA Cloud instance in trial environment.
Download the sample data from link [https://github.com/SAP-samples/datasphere-content/tree/main/SAP_Sample_Content/CSV](https://github.com/SAP-samples/datasphere-content/tree/main/SAP_Sample_Content/CSV).
Import to the HANA dadtabase.

## Adjust the schema file
Adjust the schema files under folder schema to adapt your database.

## Adjust the HANA Cloud Configuration in config.py
Adjust the HANA Cloud instance linke, user and password in config.py.
```
HC = {
    "endpoint" : "<Your HANA Cloud Instance Link>",
    "port" : 443,
    "user" : "<Your DB user>",
    "password" : "<Your DB password>"
}
```

# Run the demo
Run command:
```
#python app.py
```
Then navigate to link [http://localhost:5000](http://localhost:5000) and you can access the demo.
