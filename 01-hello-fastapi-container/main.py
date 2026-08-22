from fastapi import FastAPI

app = FastAPI(
    title="Docker Playground",
    description="01 - Hello FastAPI Container",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Hello from FastAPI inside Docker!",
        "project": "01 - Hello FastAPI Container"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
