from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the "static" directory to serve static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")
book = [{'name': '1', 'feedback': 'r3  '}, {'name': '2', 'feedback': 'dsa fsad fs'}]



# Define the main route for the landing page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    print(book)

    return templates.TemplateResponse("index.html", {"request": request, "book": book})


# Handle HTMX request to submit feedback
@app.post("/submit", response_class=JSONResponse)
async def submit_feedback(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    feedback = form_data.get("feedback")
    data = {"name": name.strip(), "feedback": feedback.strip()}
    book.append(data)
    # Process feedback (you can save it to a database, etc.)
    # For simplicity, we just return a JSON response with the submitted data.
    return templates.TemplateResponse("form.html", {"request": request, "book": book})


@app.post("/delete/{item_name}", response_class=JSONResponse)
async def delete_item(request: Request, item_name: str):
    # Find and remove the item with the specified id from the book list
    for i, item in enumerate(book):
        print(item)
        print(item_name)
        if item.get('name') == item_name:
            del book[i]
            break
    return templates.TemplateResponse("form.html", {"request": request, "book": book})
    
