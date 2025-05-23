from fastapi import FastAPI
import uvicorn
from order import router as order_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- You can change this to ["http://localhost:3000"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order_router, prefix="/orders", tags=["Orders"])

@app.get("/")
def home():
    return {"message": "Welcome to the  order-management microservice"}

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8060)
