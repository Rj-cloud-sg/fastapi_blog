from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
@app.get("/", include_in_schema=False)     #declearator
@app.get("/posts", include_in_schema=False) #Both route and /posts will execute the same function and return the same response
def home(request: Request):   # function that I'm decorating
    return templates.TemplateResponse(request=request, name="home.html", context={"posts": posts, "title": "Home"}) #returning the template response and passing the request object to the template instead of html, pass data to template (dictionary)


# Creating API endpoint that returns the list of disctionaries
@app.get("/api/posts")     
def get_posts(): 
    return posts  