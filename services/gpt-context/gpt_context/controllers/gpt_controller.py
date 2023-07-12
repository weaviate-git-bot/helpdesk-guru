from gpt_context.services.context_service import ContextService
from gpt_context.services.qa_service import QAService


class GptController:
    def __init__(self, qa_service: QAService, context_service: ContextService):
        self.qa_service = qa_service
        self.context_service = context_service

    def ask(self, query: str, conversation_id: str) -> str:
        return self.qa_service.ask(query, conversation_id)

    def clear_history(self, conversation_id: str) -> None:
        return self.qa_service.clear_history(conversation_id)

    def clear_index(self) -> None:
        return self.context_service.clear_index()

    def add_google_docs(self, folder_id: str) -> None:
        return self.context_service.add_google_docs(folder_id)
