from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path

app=FastAPI()

Data_file=Path("books.json")

def load_data():
    with open(Data_file,"r") as f:
        return json.load(f)


def save_data(data):
    with open(Data_file,"w") as f:
        json.dump(data,f,indent=4)   
class Book(BaseModel):
    title:str
    author:str
    price:int       

@app.get("/books")
def get_books():
    return {"books":load_data()}

@app.get("/books/{book_id}")
def get_book(book_id:int):
    books=load_data()
    for book in books:
        if book["id"]==book_id:
            return book
    return "Not Found"    

@app.post("/books/")
def add_book(book:Book):
    books=load_data()
    book_id=books[-1]["id"]+1
    newbook={"id":book_id,**book.dict()}
    books.append(newbook)
    save_data(books)
    return "A new book is added"
@app.put("/books/{book_id}")
def update_book(book_id:int,updatebook:Book):
    books=load_data()
    for i,book in enumerate(books):
        if book["id"]==book_id:
            books[i]={"id":book_id,**updatebook.dict()}
            save_data(books)
            return "Book updated"
    return "Book not found"

@app.delete("/books/{book_id}")
def delebook(book_id:int):
    books=load_data()
    for book in books:
        if book["id"]==book_id:
            books.remove(book)
            save_data(books)
            return "Book deleted"
    return "Book Not Found"    