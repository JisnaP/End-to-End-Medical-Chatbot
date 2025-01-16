from flask import Flask,render_template,jsonify,request
from src.helper import download_hugging_face_embedding
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import CTransformers
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from src.prompt import *
app=Flask(__name__)

PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
embeddings=download_hugging_face_embedding()
index_name="mchatbot"

doc_search=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens': 500,
                          'temperature':0.4})

retriever=doc_search.as_retriever(
                 search_type='similarity',search_kwargs={"k":3}

)
prompt=ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human",Human_prompt)
    ]
)
question_answer_chain=create_stuff_documents_chain(llm,prompt)
rag_chain=create_retrieval_chain(retriever,question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get",methods=["GET","POST"])
def chat():
    msg=request.form['msg']
    input=msg
    print(input)
    response=rag_chain.invoke({'input':msg})
    print("Response: ",response['answer'])
    return str(response['answer'])
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
