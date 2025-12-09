import uvicorn
import multiprocessing

def run_app1():
    uvicorn.run("backend/main:app", host="localhost", port=8000, reload=True)

def run_app2():
    uvicorn.run("backend/main:feelApp", host="localhost", port=9095, reload=True)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_app1)
    p2 = multiprocessing.Process(target=run_app2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
