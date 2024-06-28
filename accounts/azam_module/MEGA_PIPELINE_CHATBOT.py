import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate


# os.environ["AZURE_OPENAI_API_KEY"] = "139f48c53a084f45ae9b1b8d0c263366"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://azam-azure-openai.openai.azure.com/"


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def prompt_maker():
    system_instruction = """
As an AI assistant, try to answer the question from the provided context as much as possible.
        if no relavant information is available in the provided context then only answer the question by using your knowledge about the topic.
"""
    template = (
        f"{system_instruction} "
        "Here is the context: {context}. "
        "This is the question: {question}"
    )
    prompt = PromptTemplate.from_template(template)
    return prompt


def chatbot_init(data_dir):
    load_dotenv()
    llm = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="gpt3_endpoint")

    embedding_model = AzureOpenAIEmbeddings(
        azure_deployment="embedding_endpoint",
        openai_api_version="2023-05-15")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.listdir(data_dir):
        # Directory is empty, create sample.txt and write 'abc' to it
        with open(os.path.join(data_dir, 'sample.txt'), 'w') as file:
            file.write('.')

    loader = DirectoryLoader(data_dir, glob="*.txt", loader_cls=TextLoader)
    #loader = DirectoryLoader(data_dir)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=10)
    docs = text_splitter.split_documents(documents)

    db = FAISS.from_documents(documents=docs, embedding=embedding_model)
    db.save_local("faiss_vector_store")
    retriever = db.as_retriever()

    prompt = prompt_maker()

    rag_chain_from_docs = (
        RunnablePassthrough.assign(
            context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser())

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    return llm, embedding_model, loader, docs, db, retriever, prompt, rag_chain_with_source

def remove_profanity(sentence):
    words = sentence.split()
    profanity_words = ['shit','damn'] # sample
    clean_words = [word for word in words if word.lower() not in profanity_words]
    return ' '.join(clean_words)


def gen_answer(question, rag_chain, chat_history):
    result_json = rag_chain.invoke(question)
    print("Result JSON:", result_json)
    print(f"response = {result_json['answer']}")
    response = result_json['answer']
    response = remove_profanity(response)
    chat_history.append((question, response))
    return response, chat_history
