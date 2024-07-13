import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

drop_dict = {
    'Un planeta en emergencia': ['PRÁCTICAS ARTÍSTICAS EN UN PLANETA EN EMERGENCIAANNA L. TSING']
}

def get_pdf_text(file_path):
    text = ""
    pdf_reader = PdfReader(file_path)
    for page in pdf_reader.pages:
        text += page.extract_text().replace('''\n\'''','\n').replace('\n',' ').replace('  ',' ').replace(' - ','')
        for title in drop_dict.keys():
            if title in file_path:
                for elem in drop_dict[title]:
                    text = text.replace(elem, '')
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=250,
        chunk_overlap=20,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks, titles):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    metadata = [{"title": title} for title in titles]
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings, metadatas=metadata)
    return vectorstore

def main():
    directory = "C:\\Users\\alfredo\\Desktop\\lengua-cuerpo\\Repositorio _Las lenguas del cuerpo_"
    pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]

    all_text_chunks = []
    titles = []

    for pdf_file in pdf_files:
        print(f"Procesando {pdf_file}")
        raw_text = get_pdf_text(pdf_file)
        text_chunks = get_text_chunks(raw_text)
        all_text_chunks.extend(text_chunks)
        titles.extend([os.path.basename(pdf_file)] * len(text_chunks))

    vectorstore = get_vectorstore(all_text_chunks, titles)

    # Save the vector store to a file
    vectorstore.save_local("knowledgebase_lengua_cuerpo")

    # Example document retrievals
    retriever = vectorstore.as_retriever()
    query = "deseo saber que es la lengua de la palabra 'cuerpo'"
    results = retriever.get_relevant_documents(query)
    
    for result in results:
        print(result)

if __name__ == '__main__':
    main()