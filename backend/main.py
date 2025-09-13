import uvicorn
import db
import fastapi
from fastapi.middleware.cors import CORSMiddleware

race = "2025_restoration_run"

app = fastapi.FastAPI(
    debug=True,
    title="ChronoDash API",
    description="A REST API Enabling Awesomeness",
    version="2025.09.13",
)

origins = [
    "http://localhost:5173",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/setup", tags=["Dev Tools"])
def setup_the_database():
    db.query(
        """
        CREATE TABLE IF NOT EXISTS runner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            race TEXT,
            first_name TEXT,
            last_name TEXT,
            bib TEXT,
            race_division TEXT,
            start TIMESTAMP,
            finish TIMESTAMP,
            email TEXT,
            phone TEXT,
            checked_in INT DEFAULT 0,
            visible INT DEFAULT 1
        );
        """, 
        commit=True
    )
    db.query(
        """
        CREATE TABLE IF NOT EXISTS raw_event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            data TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """, 
        commit=True
    )
    db.query(
        """
        CREATE TABLE IF NOT EXISTS config (
            race TEXT PRIMARY KEY,
            mode TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            visible INT DEFAULT 1
        );
        """, 
        commit=True
    )
    db.query("INSERT INTO config (race, mode) VALUES (?, 'init')", (race,), commit=True)
    


@app.get("/mode/{new_mode}", tags=["Frontend"])
def set_the_mode(new_mode:str):
    db.query("UPDATE config SET mode=? WHERE race = ?", (new_mode, race), commit=True)
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
