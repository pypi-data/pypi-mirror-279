from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
from langchain.memory import ConversationBufferMemory as LangchainConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory as LangchainStreamlitChatMessageHistory
from typing import Dict, Any

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.write(self.text.replace('\\n','    \\n    ')[1:-1])
        # print("Callback: " + self.text.replace('\\n','    \\n    ')[1:-1])
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        # print(f"Callback - Chain End: {outputs}")
        self.container.write(outputs["output.json"])

class ConversationBufferMemory(LangchainConversationBufferMemory):
    pass

class StreamlitChatMessageHistory(LangchainStreamlitChatMessageHistory):
    pass