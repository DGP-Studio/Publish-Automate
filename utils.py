import httpx
import os


def download_stream_file(url, file_name):
    os.makedirs("./cache", exist_ok=True)
    with httpx.stream("GET", url) as r:
        with open(f"./cache/{file_name}", "wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)


def send_zulip_message(message: str):
    zulip_url = "https://hutao.zulipchat.com/api/v1/messages"
    BOT_EMAIL_ADDRESS = os.getenv("ZULIP_EMAIL")
    BOT_API_KEY = os.getenv("ZULIP_API_KEY")
    zulip_stream = os.getenv("ZULIP_STREAM")
    zulip_topic = os.getenv("ZULIP_TOPIC")

    data = {
        "type": "stream",
        "to": zulip_stream,
        "topic": zulip_topic,
        "content": message
    }

    client = httpx.Client(auth=(BOT_EMAIL_ADDRESS, BOT_API_KEY))

    response = client.post(zulip_url, data=data)
    print(response.status_code)
    print(response.text)
    return True
