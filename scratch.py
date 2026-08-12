import httpx

from app.config import settings

resp = httpx.post(
    f"{settings.openai_base_url}/chat/completions",
    headers={
        "Authorization": f"Bearer {settings.openai_api_key.get_secret_value()}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-5.4",
    },
)

print("status:", resp.status_code)
print("headers:", dict(resp.headers))
print("body:", resp.text)
