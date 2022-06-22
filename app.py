from flask import Flask,request,Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings
import asyncio
import os

from echobot import EchoBot

app = Flask(__name__)
loop = asyncio.get_event_loop()

PORT = 5000
APP_ID = os.environ.get("MicrosoftAppId", "32465065-e5a7-4458-9977-9fa9f9d2bf12")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "042e901d-559b-431e-a0ac-5695a6d77284")

botadaptersettings = BotFrameworkAdapterSettings(APP_ID,APP_PASSWORD)
botadapter = BotFrameworkAdapter(botadaptersettings)

ebot = EchoBot()

@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
      jsonmessage = request.json
    else:
      return Response(status=415)

    activity = Activity().deserialize(jsonmessage)

    async def turn_call(turn_context):
        await ebot.on_turn(turn_context)

    task = loop.create_task(botadapter.process_activity(activity,"",turn_call))
    loop.run_until_complete(task)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=PORT)

