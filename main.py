from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


posts: list[dict] = [
    {
        "id": 1,
        "author": "Ronnie Spencer",
        "title": "First FastApi project",
        "content": "Learning modern frameworks",
        "date_posted": "June 1, 2026"
    },
    {
        "id": 2,
        "author": "John Doe",
        "title": "Python is the best first language to learn",
        "content": "Building websites is a great skill",
        "date_posted": "June 1, 2026"
    },
]


# Create first route
@app.get("/", response_class=HTMLResponse, include_in_schema=False)     #decoclearator
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False) #Both route and /posts will execute the same function and return the same response
def home():   # function that I'm decorating
    return f"<h1>{posts[0]['title']}</h1>"  #dictionary that will be converted to JSON and sent as a response


# Creating API endpoint that returns the list of disctionaries
@app.get("/api/posts")     
def get_posts(): 
    return posts  