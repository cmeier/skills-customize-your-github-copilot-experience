"""
Starter code for FastAPI REST APIs assignment

This is a basic FastAPI application template to help you get started.
Complete the TODO sections to implement the required functionality.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# Create FastAPI application instance
app = FastAPI(
    title="Student API",
    description="A simple REST API for managing students",
    version="1.0.0"
)

# TODO: Define Pydantic models for request/response validation
class StudentBase(BaseModel):
    """Base model for student data"""
    name: str
    grade: int
    email: Optional[str] = None


class StudentCreate(StudentBase):
    """Model for creating a new student"""
    pass


class Student(StudentBase):
    """Model for student response"""
    id: int

    class Config:
        from_attributes = True


# In-memory storage (replace with database in production)
students_db: dict = {}
next_id = 1


# TODO: Task 1 - Create basic GET endpoint
@app.get("/", tags=["Welcome"])
async def read_root():
    """Welcome endpoint"""
    return {"message": "Welcome to the Student API"}


@app.get("/students", response_model=List[Student], tags=["Students"])
async def list_students():
    """Get all students"""
    # TODO: Implement this endpoint to return all students
    return list(students_db.values())


@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
async def get_student(student_id: int):
    """Get a specific student by ID"""
    # TODO: Implement error handling for student not found
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return students_db[student_id]


# TODO: Task 1 - Create basic POST endpoint
@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: StudentCreate):
    """Create a new student"""
    # TODO: Implement student creation with ID generation
    global next_id
    new_student = Student(id=next_id, **student.dict())
    students_db[next_id] = new_student
    next_id += 1
    return new_student


# TODO: Task 2 - Add PUT endpoint for updating
@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
async def update_student(student_id: int, student: StudentCreate):
    """Update an existing student"""
    # TODO: Implement student update with proper error handling
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    updated_student = Student(id=student_id, **student.dict())
    students_db[student_id] = updated_student
    return updated_student


# TODO: Task 2 - Add DELETE endpoint for removing
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(student_id: int):
    """Delete a student"""
    # TODO: Implement student deletion with proper error handling
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    del students_db[student_id]


# Run the application with: uvicorn starter-code:app --reload
