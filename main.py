import time
import os
from fastapi import FastAPI
from PyPDF2 import PdfReader
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

book_name = "Building Machine Learning Systems with Python - Second Edition.pdf"


def text_streamer(file_path: str):
    with open(file_path, "r") as f:
        for line in f:
            yield line


def pdf_streamer(file_path: str):
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            for line in text.splitlines():
                time.sleep(1)
                yield line


@app.get('/read-book')
def read_book():
    book_path = os.path.join(
        ".", "Building Machine Learning Systems with Python - Second Edition.pdf")
    return StreamingResponse(pdf_streamer(file_path=book_path), media_type="text/plain")
