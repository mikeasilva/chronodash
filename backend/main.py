import uvicorn
import fastapi
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI(debug=True)

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
