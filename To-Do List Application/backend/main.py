from pymongo import MongoClient
from models import User, Task, UserLogin, UserTasks
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")

db = client["genai"]
users_collections = db["users"]
task_collections = db["tasks"]

user_id = None

def verify_password(input_password, user_password):
    return input_password == user_password

@app.post("/register/")
def new_user(user: User):
    result = users_collections.insert_one(user.dict())
    return {"user_id": str(result.inserted_id)}
    
@app.post("/login/")
def get_user(user: UserLogin):
    result = users_collections.find_one({"email": user.email})

    if not result:
        print("User not found")
    
    if not verify_password(user.password, result["password"]):
        print("Invalid Password")
    
    return {"user_id": str(result["_id"]), "message": "Login successful"}

@app.post("/new_task/")
def new_task(tasks: Task):
    result = task_collections.insert_one(tasks.dict())

    return "Successful!"

@app.post("/get_tasks/")
def get_all_tasks(user: UserTasks):
    tasks = list(task_collections.find({"user_id": user.user_id}))
    for task in tasks:
        task["_id"] = str(task["_id"])  # Convert ObjectId to string
    return jsonable_encoder(tasks)