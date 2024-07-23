from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routers import users, cart, products, categories, loans
from pathlib import Path
from .config import templates

app = FastAPI()

static_files_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    message = request.cookies.get("message")
    context = {"request": request}
    if message:
        context["message"] = message
    return templates.TemplateResponse("index.html", context)

@app.get("/messages/", response_class=HTMLResponse)
def get_message(request:Request):
    message = request.cookies.get("message")
    context = {
        "request": request,
        "message": message
    }
    return templates.TemplateResponse("messages.html", context)

app.include_router(products.router, prefix="/produtos", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(loans.router, prefix="", tags=["loans"])