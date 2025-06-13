from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/health")
def health_status():
    return {"message": "Application is running"}
