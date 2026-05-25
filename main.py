from fastapi import FastAPI
from db_config.db import Base, engine
from routers import auth, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clean Role Architecture Backend",
    description="A polished decoupled REST engine utilizing custom modular routing systems.",
    version="2.0.0"
)


app.include_router(auth.router, prefix="/auth")
app.include_router(tasks.router, prefix="/tasks")

@app.get('/root', tags=["Health Checks"])
def root():
    return {'status': 'backend operational'}
