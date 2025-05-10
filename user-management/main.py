from fastapi import FastAPI
import uvicorn
from user import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def home():
    return {"message": "Welcome to the user-management microservice"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050)
