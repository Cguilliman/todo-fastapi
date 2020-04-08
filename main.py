from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"Title": "hello"}


@app.get("/item/{item_id}")
def read_item(item_id, q=None):
    return {"item_id": item_id, "q": q}
