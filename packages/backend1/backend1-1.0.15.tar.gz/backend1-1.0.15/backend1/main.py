import uvicorn
from fastapi import FastAPI
from backend1.routers.users import router as users_router
from backend1.routers.test import router as test_router
from backend1.routers.table import router as table_router
from fastapi.middleware.cors import CORSMiddleware
from backend1.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url="/backend1/openapi.json",
    docs_url="/backend1/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(test_router)
app.include_router(table_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

