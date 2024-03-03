"""
Services common to all files
"""

from langchain_community.llms import OpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import azure_api_key, azure_endpoint


def api_call(system_message, human_message):
    try:
        llm = AzureChatOpenAI(
            openai_api_version="2023-05-15",
            azure_deployment="gpt-35-turbo",
            api_key=azure_api_key,
            azure_endpoint=azure_endpoint,
        )

        msg = [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message),
        ]

        res = llm(messages=msg)
        return res.content

    except Exception as e:
        print("Error in api_call: ", e)
        return None
