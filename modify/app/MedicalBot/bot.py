# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import requests

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        endpoint_kb = 'https://ce5d64460217.ngrok.io/proc-nlu-kb'

        input_text = str(turn_context.activity.text)
        input_id = str(turn_context.activity.conversation.id)

        dict_input = {}

        dict_input['mess'] = input_text
        dict_input['_id'] = input_id

        response_object = requests.post(url=endpoint_kb, json=dict_input)

        response_object_json = response_object.json()

        response_message = response_object_json['predict']['original_text']

        await turn_context.send_activity(response_message)

        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Xin chào mình là Medical Bot, mình có thể giúp gì được cho bạn ?")
