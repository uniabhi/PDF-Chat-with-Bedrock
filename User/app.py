import boto3
import streamlit as st
import os
import uuid

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"  # Replace with your preferred region where Bedrock is available
)

## s3_client
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

## Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_aws import BedrockLLM

## prompt and chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

## Text Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## import FAISS
from langchain_community.vectorstores import FAISS


bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)

folder_path="/tmp/"

def get_unique_id():
    return str(uuid.uuid4())

## load index
def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

def get_llm():
    llm = BedrockLLM(
        model_id="meta.llama3-8b-instruct-v1:0", 
        client=bedrock_client,
        model_kwargs={
            'max_gen_len': 512,  # For Llama 3, use max_gen_len instead
            'temperature': 0.7
        }
    )
    return llm

# get_response()
def get_response(llm,vectorstore, question ):
    ## create prompt / template
    prompt_template = """

    Human: Please use the given context to provide concise answer to the question
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer = qa.invoke({"query": question})
    return answer['result']


## main method
def main():
    st.header("This is Client Site for Chat with PDF demo using Bedrock, RAG etc")

    load_index()

    dir_list = os.listdir(folder_path)
    st.write(f"Files and Directories in {folder_path}")
    st.write(dir_list)

    ## create index
    faiss_index = FAISS.load_local(
        index_name="my_faiss",
        folder_path = folder_path,
        embeddings=bedrock_embeddings,
        allow_dangerous_deserialization=True
    )

    st.write("INDEX IS READY")
    question = st.text_input("Please ask your question")
    if st.button("Ask Question"):
        with st.spinner("Querying..."):

            llm = get_llm()

            # get_response
            st.write(get_response(llm, faiss_index, question))
            st.success("Done")

if __name__ == "__main__":
    main()