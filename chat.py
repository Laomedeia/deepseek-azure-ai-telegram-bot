import os
import logging
import asyncio
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize the client
client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_KEY"])
)

# Get max tokens from environment or use default
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))

# Store conversation history for each user
conversations = {}

# Create a thread pool executor for running sync code
executor = ThreadPoolExecutor()

async def handle_message(message: str, user_id: str = "default") -> str:
    """
    Process the incoming message and return a response using Azure AI
    """
    try:
        logger.info(f"Processing message for user {user_id}")
        
        # Initialize or get user's conversation history
        if user_id not in conversations:
            logger.info(f"Initializing new conversation for user {user_id}")
            conversations[user_id] = []
        
        # Add user message to history
        conversations[user_id].append({
            "role": "user",
            "content": message
        })

        # Prepare messages payload
        payload = {
            "messages": conversations[user_id],
            "max_tokens": MAX_TOKENS
        }

        logger.info(f"Sending request to Azure AI for user {user_id}")
        # Run the synchronous Azure AI call in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            executor,
            lambda: client.complete(payload)
        )
        
        # Add assistant's response to history
        assistant_message = response.choices[0].message.content
        conversations[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })

        # Keep only last N messages to prevent context from growing too large
        if len(conversations[user_id]) > 10:
            conversations[user_id] = conversations[user_id][-10:]
            logger.info(f"Trimmed conversation history for user {user_id}")

        logger.info(f"Successfully processed message for user {user_id}")
        return assistant_message

    except Exception as e:
        logger.error(f"Error in handle_message for user {user_id}: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller
