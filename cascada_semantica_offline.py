import os
import time
import sys
import random
import threading
import openai

# AQUÍ VA LA LLAVE - descomenta la próxima linea
# openai.api_key = ''

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

# List of body-instruction strings
body_instructions = [
    "un cuerpo debe explorarse para modificarse y entenderse\nexploremos\ntoma la cámara\nve primero a la cara, muéstrame tus ojos\nte estamos escaneando",
    "allí donde no se ve con tanta claridad hay que echar luz. Un cuerpo debe desprender su prótesis, necesita de otro cuerpo para lograrlo",
    "un cuerpo debe Inyectarse “lenguicliterona”  para modificar su entorno",
    "un cuerpo transmite otro cuerpo y se desprende para llegar a la metamorfosis",
]

stop_event = threading.Event()

def load_vectorstore(directory):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(directory, embeddings)
    return vectorstore

def get_retriever():
    vectorstore = load_vectorstore("knowledgebase_lengua_cuerpo")
    retriever = vectorstore.as_retriever(search_kwargs={'k':50})
    return retriever

dots = ['', '.', '. .', '. . .']

def waterfall_display(body_instruction):
    lines = body_instruction.split('\n')
    for line in lines:
        # Three-dot animation
        for _ in range(random.randint(5, 15)):  # Randomly long loop
            loading_char = random.choice(' .-/*^#~')
            sys.stdout.write(f"\r\033[1;34m{loading_char}\033[0m")
            sys.stdout.write('\b')
            sys.stdout.flush()
            time.sleep(0.5)
        
        # instruction anumatuion 
        words = line.split()
        words.insert(0, "~")
        for word in words:
            sys.stdout.write(f"\033[1;34m{word}\033[0m ")  # Blue highlight
            sys.stdout.flush()
            time.sleep(random.uniform(0.8, 1.5))
        print()
        sys.stdout.flush()
        print("\r\033[1;34m   \033[0m", end='')  # Clear the line after animation
    print()

def cyberpunk_display(results):
    for result in results:
        text = result.page_content.replace('- ','')
        words = text.split()
        for word in words:
            if stop_event.is_set():
                break
            if random.random() < 0.1:  # 10% chance to highlight a word
                sys.stdout.write(f"\033[1;32m{word}\033[0m ")  # Green highlight
            else:
                for letter in word:
                    if stop_event.is_set():
                        break
                    # Glitch effect: type random characters before the actual letter
                    for _ in range(random.randint(1, 5)):
                        sys.stdout.write(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'))
                        sys.stdout.flush()
                        time.sleep(random.uniform(0.02, 0.07))
                        sys.stdout.write('\b')  # Backspace to remove the random character
                    sys.stdout.write(letter)
                    sys.stdout.flush()
                    time.sleep(random.uniform(0.02, 0.09))
                sys.stdout.write(' ')
            sys.stdout.flush()
            time.sleep(random.uniform(0.02, 0.05))
        print()

        sys.stdout.flush()
        if stop_event.is_set():
            break

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal content

def listen_for_enter():
    input()
    stop_event.set()

def main():
    retriever = get_retriever()
    body_instruction_index = -1
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal content

        query = input("\n\n")
        if query.lower() in ['exit', 'quit']:
            break
        print()
        
        # Display a body instruction
        body_instruction_index += 1
        body_instruction = body_instructions[body_instruction_index]
        results = retriever.get_relevant_documents(query)
        
        waterfall_display(body_instruction)

        stop_event.clear()
        enter_thread = threading.Thread(target=listen_for_enter)
        enter_thread.start()

        display_thread = threading.Thread(target=cyberpunk_display, args=(results,))
        display_thread.start()
        display_thread.join()
        
        enter_thread.join()
        stop_event.clear()
        
 
if __name__ == '__main__':
    main()