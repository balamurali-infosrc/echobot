from fastapi import FastAPI, Request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import os

app = FastAPI()

# Load credentials
APP_ID = os.getenv("MICROSOFTAPPID", "")
APP_PASSWORD = os.getenv("MICROSOFTAPPPASSWORD", "")
TENANT_ID = os.getenv("MICROSOFTAPPTENANTID", "")

# Adapter settings (required for Single Tenant Azure bots)
settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
settings.channel_auth_tenant = TENANT_ID
settings.oauth_scope = "https://api.botframework.com/.default"

adapter = BotFrameworkAdapter(settings)


async def bot_logic(turn_context: TurnContext):
    # Respond ONLY to actual user messages
    if turn_context.activity.type == "message":
        await turn_context.send_activity(f"You said: {turn_context.activity.text}")
    # Ignore everything else (no Bot connected messages)
    return


@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    await adapter.process_activity(activity, auth_header, bot_logic)
    return Response(status_code=200)
