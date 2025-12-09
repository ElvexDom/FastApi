import uvicorn
import multiprocessing
import os
from dotenv import load_dotenv

load_dotenv()

FAST_API_PORT = int(os.getenv("FAST_API_PORT", "8080"))
API_BASE_URL = os.getenv('API_BASE_URL')

def run_app1():
    uvicorn.run(
    "backend.main:app", 
    host = API_BASE_URL,
    port = FAST_API_PORT,
    reload = True
    )

def run_app2():
    uvicorn.run(
    "backend.sentiment_api:feelApp", 
    host = API_BASE_URL,
    port = FAST_API_PORT+1, 
    reload = True
    )


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_app1)
    p2 = multiprocessing.Process(target=run_app2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
