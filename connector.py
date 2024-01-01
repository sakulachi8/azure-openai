import os

import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.environ["OPENAI_API_TYPE"]
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.environ["OPENAI_API_BASE"]
openai.api_version = os.environ["OPENAI_API_VERSION"]
search_endpoint = os.environ["SEARCH_ENDPOINT"]
search_key = os.environ["SEARCH_KEY"]
index_name = os.environ["INDEX_NAME"]


def get_search_connection(index=index_name):
    credential = AzureKeyCredential(search_key)
    client = SearchClient(endpoint=search_endpoint, index_name=index, credential=credential)
    return client

def save_embedding_to_search(documents, index=index_name):
    client = get_search_connection(index)
    client.upload_documents(documents=documents)
    client.close()

def search_documents(search_text, index=index_name):
    client = get_search_connection(index)
    results = client.search(search_text)
    client.close()
    return results

def request_to_model(input, index=index_name):
    prompt = input.messages[-1].content
    # drop proposal_model from input
    my_context = list(search_documents(prompt, index))[:5]
    search_content = ''
    context_list = []
    for item in my_context:
        search_content += f"```\n {item['content']} \n```"
    context_list.append({"role": "system", "content": f"""You are an expert legal assistant. You will explain contract terms using the technical manual provided as context. Do not add any information that is not directly relevant to the question, or not supported by the context provided. But the content is too long and too technical. The customer needs to hear a brief, actionable summary.
Respond only from the context provided and only in French.
Do not give any information about process or fields that is not mentioned in the PROVIDED CONTEXT.
### CONTEXT:
{search_content[:10000]}

### END OF CONTEXT

Example of a question:
Q: What is politics?
A: requête hors contexte.
"""})
    context_list.append({"role": "user", "content": "What is politics?"})
    context_list.append({"role": "assistant", "content": "requête hors contexte."})
    for item in context_list + list(input.messages):
        print(dict(item)['role'])
    response = openai.chat.completions.create(
        messages=context_list + input.messages,
        model=input.model,
        max_tokens=input.max_tokens,
        temperature=input.temperature,
        top_p=input.top_p
    )
    return response
