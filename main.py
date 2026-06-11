from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") #mounting the static directory to serve static files like css, js, images

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
@app.get("/", include_in_schema=False, name="home")     #declearator
@app.get("/posts", include_in_schema=False, name="posts") #Both route and /posts will execute the same function and return the same response
def home(request: Request):   # function that I'm decorating
    return templates.TemplateResponse(request=request, 
    name="home.html", 
    context={"posts": posts, "title": "Home"}) #returning the template response and passing the request object to the template instead of html, pass data to template (dictionary)

@app.get("/posts/{post_id}", include_in_schema=False,) # passes in post id (inside curly braces is the path parameter)     
def post_page(request: Request, post_id: int): 
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(request=request, 
              name="post.html", 
              context={"post": post, "title": title},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

# Creating API endpoint that returns the list of disctionaries
@app.get("/api/posts")     
def get_posts(): 
    return posts  

@app.get("/api/posts/{post_id}") # passes in post id (inside curly braces is the path parameter)     
def get_posts(post_id: int): 
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
    
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
