from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="IP Image Puller")

@app.get("/")
async def root():
    return {"message": "IP Image Puller API is running!"}

# Example route
@app.get("/ip")
async def get_ip(request: Request):
    client_host = request.client.host
    return {"your_ip": client_host}
