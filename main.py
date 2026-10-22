from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import HTTPException

app =  FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        return {"message": "Database connected successfully"}

notes = [{
    "id": 1,
    "title": "Hello",
    "content": "Python AI Eng"
}]


class NoteCreate(BaseModel):
    title: str = Field(min_length =3, max_length = 40)
    content: str = Field(min_length = 2, max_length = 1000)

class NoteResponse(BaseModel):
    id: number;
    title: string;
    content: string

@app.post("/notes")
def create_notes(note: NoteCreate):
    new_notes = {
        "id": len(notes) + 1,
        "title": note.title,
        "content": note.content
    }
    notes.append(new_notes)
    return new_notes

@app.get("/get_notes")
def display_notes():
    return notes;


@app.get("/note/{note_id}")
def getNotesById(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    
    raise HTTPException(status_code = 404, detail = "Note not found!")

@app.put("/note/update/{note_id}")
def updateNotesById(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = "New title"
            note["content"] = "Hey there! here is new content!"
            return note

    raise HTTPException(status_code = 404, detail = "Notes not found!")

@app.delete("/note/delete/{note_id}")
def deleteNoteById(note_id: int):
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            deletedNote = notes.pop(i)
            return {
                "message": "Note deleted", "note": deletedNote
            }
    raise HTTPException(
        status_code = 404, detail = "Note not found to delete"
    )

@app.get("/notes/search")
def search_notes(search: str):
    result = []
    for note in notes:
        if search.lower() in note["title"].lower():
            result.append(note)
    return result