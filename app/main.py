from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import users, cart, products, categories
from pathlib import Path
import logging
from .config import templates

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

static_files_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the database tables
#@app.on_event("startup")
#def on_startup():
#   init_db()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    welcome_message = request.cookies.get("welcome_message")
    context = {"request": request}
    if welcome_message:
        context["welcome_message"] = welcome_message
    return templates.TemplateResponse("categorias/index.html", context)

app.include_router(products.router, prefix="/produtos", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])

'''
# Include routers for different modules
app.include_router(auth.router, prefix="/auth", tags=["auth"])
'''