from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

students = {
    1:{
        "name": "Rohit",
        "age":22,
        "year": "sde"
    },
    2:{
        "name": "Mohit",
        "age":19,
        "year": "hehe"
    }
}

@app.get("/")
def index():
    return {"name": "First Data"}

@app.get("/get-all-students")
def get_all_students():
    all_students = []
    for id in students:
        all_students.append(students[id])
    return all_students

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of the student you want to view", gt=0, lt=999)):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test: int):
    for id in students:
        if students[id]["name"] == name:
            return {"id": student_id,"data": students[id]}
    return {"Data": "Not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "Student Exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"error": "Student does not exist"}
    
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"error": "Student does not exist"}
    del students[student_id]
    return {"msg": "Deletion Successful"}