from fastapi import FastAPI, Request
import requests

app = FastAPI()

WEBHOOK_URL = "PUT_YOUR_WEBHOOK_HERE"

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def handle_request(request: Request, path: str):
    try:
        ip = request.headers.get("x-forwarded-for", request.client.host)
        user_agent = request.headers.get("user-agent")

        data = {
            "ip": ip,
            "user_agent": user_agent,
            "path": path,
            "method": request.method
        }

        # send to webhook
        requests.post(WEBHOOK_URL, json=data)

        return {
            "status": "ok"
        }

    except Exception as e:
        return {"error": str(e)}
