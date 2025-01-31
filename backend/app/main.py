from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User as model_User, Task as TaskModel
from schemas import UserCreate, TaskCreate, Task, User as schemas_User
from crud import get_user_by_username, create_user, get_tasks, create_task
from auth import create_access_token, verify_password, SECRET_KEY, ALGORITHM
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Добавляем CORSMiddleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/register")
@app.options("/login")
def preflight_handler():
    return {"message": "Preflight check successful"}


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> schemas_User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas_User.from_orm(db_user)


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)


@app.post("/login")
def login(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/tasks/", response_model=Task)
def create_new_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: model_User = Depends(get_current_user),
):
    created_task = create_task(db, task, current_user.id)
    return Task.from_orm(created_task)


@app.get("/tasks/", response_model=list[Task])
def get_all_tasks(
        db: Session = Depends(get_db),
        current_user: model_User = Depends(get_current_user),
):
    tasks = get_tasks(db, current_user.id)
    return [Task.from_orm(task) for task in tasks]
