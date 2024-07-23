from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, crud, auth
from ..database import get_db
from ..config import templates

router = APIRouter()

@router.get("/cadastro", response_class=HTMLResponse,)
def get_register(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    user = None
    if token:
        try:
            user = auth.get_current_user(token, db)
        except HTTPException as e:
            # Trate a exceção se o token estiver presente, mas for inválido
            raise HTTPException(status_code=e.status_code, detail=f"Problema de autenticação: {e.detail}")

    if user:
        context = {
            "message": "Seu login já está ativo! Deseja fazer o logoff?",
            "request": request
        }
        return templates.TemplateResponse("login.html", context)
    return templates.TemplateResponse("cadastro.html", {"request": request})

def get_cliente_form(
    cpf: str = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    data_nascimento: str = Form(...),
    password: str = Form(...)
) -> schemas.ClienteCreate:
    return schemas.ClienteCreate(
        cpf=cpf,
        nome=nome,
        email=email,
        telefone=telefone,
        data_nascimento=data_nascimento,
        password=password
    )

@router.post("/cadastro_user/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate = Depends(get_cliente_form), db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente.cpf)
    if db_cliente:
        raise HTTPException(status_code=400, detail="CPF já registrado")
    new_cliente = crud.create_cliente(db=db, cliente=cliente)

    access_token = auth.create_access_token(data={"sub": new_cliente.email}, expires_delta=timedelta(minutes=60))
    # Redireciona para a página principal com uma mensagem de boas-vindas
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="cpf", value=new_cliente.cpf, httponly=True)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="message", value=f"Bem vindo {new_cliente.nome}!", expires=timedelta(minutes=1))
    return response

@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    user = None
    if token:
        try:
            user = auth.get_current_user(token, db)
        except HTTPException as e:
            # Trate a exceção se o token estiver presente, mas for inválido
            raise HTTPException(status_code=e.status_code, detail=f"Problema de autenticação: {e.detail}")

    if user:
        context = {
            "message": "Seu login já está ativo! Deseja fazer o logoff?",
            "request": request
        }
        return templates.TemplateResponse("login.html", context)
    else:
        # Trata o caso onde não há usuário logado ou o token é inválido
        context = {
            "request": request,
            "next": "/"
        }
        return templates.TemplateResponse("login.html", context)


@router.post("/login_user/")
def login(email: str = Form(...), password: str = Form(...), next: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_cliente_by_email(db, cliente_email=email)
    if not user:
        response = RedirectResponse(url=f"/users/login?next={next}", status_code=303)
        response.set_cookie(key="error", value=f"Email incorreto", max_age=3600)
        return response
    if not auth.verify_password(password, user.password):
        response = RedirectResponse(url=f"/users/login?next={next}", status_code=303)
        response.set_cookie(key="error", value=f"senha incorreta", max_age=3600)
        return response

    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=60))
    response = RedirectResponse(url=next, status_code=303)
    response.set_cookie(key="cpf", value=user.cpf, httponly=True, max_age=3600)
    response.set_cookie(key="message", value=f"Bem vindo {user.nome}!", max_age=3600)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=3600)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/users/login")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="message")
    response.delete_cookie(key="cpf")
    return response