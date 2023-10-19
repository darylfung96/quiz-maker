from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

import poe
import PyPDF2
import time

class Text(BaseModel):
    text: str


app = FastAPI()
client = poe.Client(os.environ['POE_API_KEY'])
print(client.bot_names)

def generate_quiz(text):
    chunk_size = 1024 + 512
    step_size = chunk_size - 64
    # quiz_type = ['short answers', 'multiple choices', 'true/false']
    quiz_type = ['multiple choices']
    num_questions = 5

    client.send_chat_break('chinchilla')
    all_responses = ""
    for i in range(0, len(text), step_size):
        request = text[i: i + chunk_size]
        request += '\n\n'
        # request += f'Make ' \
        #            f'{num_questions} {quiz_type[0]}, {num_questions} {quiz_type[1]}, {num_questions} {quiz_type[2]} ' \
        #            f'quiz out of this. Show questions then the answers.'
        request += f'Make ' \
                   f'{quiz_type[0]}' \
                   f'quiz out of this. Show questions then the answers.'
        for chunk in client.send_message('chinchilla', request):
            pass
            response = chunk['text']
        all_responses += response
        print(response)
        time.sleep(5)
    return all_responses


@app.get("/generate_response")
async def generate_response(text: Text):
    generate_quiz(text)


document = ""
with open('KPER.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    num_pages = len(reader.pages)
    for i in range(num_pages):
        document += reader.pages[i].extract_text()

document = document.replace('Ch.', 'CH.')
document = document.replace('ch.', 'CH.')
chapters = document.split("CH.")[1:]

for chapter in chapters[3:]:
    current_chapter = chapter[:chapter.find('\n')]
    print(f'CHAPTER {current_chapter}')
    print(f'==========================================================')
    print(generate_quiz(chapter))
