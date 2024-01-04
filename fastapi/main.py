from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the "static" directory to serve static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Define the main route for the landing page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the main route for the feedback form
@app.get("/book", response_class=HTMLResponse)
async def read_book(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Handle HTMX request to submit feedback
@app.post("/submit-feedback", response_class=JSONResponse)
async def submit_feedback(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    feedback = form_data.get("feedback")

    # Process feedback (you can save it to a database, etc.)
    # For simplicity, we just return a JSON response with the submitted data.
    return {"name": name, "feedback": feedback}