from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
#Load the pdf file
def load_pdf(data):
     loader= DirectoryLoader(data,glob="*.pdf",
                    loader_cls=PyPDFLoader)
     documents=loader.load()
     return documents
#Split document into chunks
def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
    chunks=text_splitter.split_documents(extracted_data)
    return chunks
#Download the embeddings form Huggingface
def download_hugging_face_embedding():
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings