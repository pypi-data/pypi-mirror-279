from typing import List, Optional

from langflow.custom import CustomComponent
from langflow.memory import get_messages
from langflow.schema import Record


class MessageHistoryComponent(CustomComponent):
    display_name = "Memory"
    description = "Retrieves stored chat messages."

    def build_config(self):
        return {
            "sender": {
                "options": ["Machine", "User", "Machine and User"],
                "display_name": "Sender Type",
                "advanced": True,
            },
            "sender_name": {"display_name": "Sender Name", "advanced": True},
            "n_messages": {
                "display_name": "Number of Messages",
                "info": "Number of messages to retrieve.",
                "advanced": True,
            },
            "session_id": {
                "display_name": "Session ID",
                "info": "Session ID of the chat history.",
                "input_types": ["Text"],
                "advanced": True,
            },
            "order": {
                "options": ["Ascending", "Descending"],
                "display_name": "Order",
                "info": "Order of the messages.",
                "advanced": True,
            },
        }

    def build(
        self,
        sender: Optional[str] = "Machine and User",
        sender_name: Optional[str] = None,
        session_id: Optional[str] = None,
        n_messages: int = 100,
        order: Optional[str] = "Descending",
    ) -> List[Record]:
        order = "DESC" if order == "Descending" else "ASC"
        if sender == "Machine and User":
            sender = None
        messages = get_messages(
            sender=sender,
            sender_name=sender_name,
            session_id=session_id,
            limit=n_messages,
            order=order,
        )
        self.status = messages
        return messages
