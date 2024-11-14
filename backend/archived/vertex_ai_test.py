import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
from dotenv import load_dotenv
import os


def multiturn_generate_content():
    vertexai.init(project="motivational-chatbot-439123", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    chat = model.start_chat()
    print(chat.send_message(
        ["""hello"""],
        generation_config=generation_config,
        safety_settings=safety_settings
    ))
    print(chat.send_message(
        ["""can you say something motivational?"""],
        generation_config=generation_config,
        safety_settings=safety_settings
    ))


generation_config = {
    "max_output_tokens": 150,
    "temperature": 1.5,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

multiturn_generate_content()