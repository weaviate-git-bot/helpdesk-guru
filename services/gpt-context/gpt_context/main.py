import os
import asyncio
from grpclib.server import Server
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

from gpt_context.adapters import WeaviateVectorStoreAdapter
from gpt_context.controllers import GptController
from gpt_context.api.gpt_grpc_service import GptGrpcService
from gpt_context.services import ContextService, QAService

load_dotenv()

model_name = os.environ.get('OPENAI_MODEL')
default_port = os.environ.get('PORT') or 50051


async def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    weaviate_url = os.environ.get("WEAVIATE_URL") or "http://localhost:8080"

    store = WeaviateVectorStoreAdapter(weaviate_url, embedding=OpenAIEmbeddings())
    context_service = ContextService(store)
    qa_service = QAService(model_name, store)

    gpt_controller = GptController(qa_service, context_service)

    gpt_grpc_service = GptGrpcService(gpt_controller)

    server = Server([gpt_grpc_service])
    await server.start("0.0.0.0", default_port)
    print(f"Server started on {default_port}")
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
