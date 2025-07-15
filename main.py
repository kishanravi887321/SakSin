from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Define user model
class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

# 1️⃣ POST - Create a user
@app.post("/create-user/")
def create_user(user: User):
    return {"message": f"User {user.name} created successfully!"}

# 2️⃣ GET - Home route
@app.get("/")
def read_home():
    return {"message": "Welcome to the FastAPI Playground!"}

# 3️⃣ GET - Get all users (dummy)
@app.get("/users/")
def get_users():
    return [{"name": "Ravi"}, {"name": "Neha"}]

# 4️⃣ GET - Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "Sample User"}

# 5️⃣ PUT - Update user
@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: User):
    return {"message": f"User {user_id} updated!", "updated_data": user}

# 6️⃣ DELETE - Delete user
@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted."}

# 7️⃣ POST - Login route
@app.post("/login/")
def login(username: str, password: str):
    if username == "admin" and password == "123":
        return {"message": "Login successful!"}
    return {"message": "Invalid credentials"}

# 8️⃣ GET - Get app status
@app.get("/status/")
def get_status():
    return {"status": "running", "version": "1.0.0"}

# 9️⃣ GET - Search user
@app.get("/search/")
def search_user(name: str):
    return {"searched_for": name, "result": f"Fake result for {name}"}

# 🔟 POST - Feedback
class Feedback(BaseModel):
    comment: str
    rating: int

@app.post("/feedback/")
def submit_feedback(feedback: Feedback):
    return {"message": "Thanks for your feedback!", "data": feedback}
