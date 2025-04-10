from fastapi import FastAPI
from auth import router as auth_router
from location import router as location_router  
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(location_router, prefix="/location", tags=["Location"])

@app.get("/")
def root():
    return {"message": "location de matériel"}
