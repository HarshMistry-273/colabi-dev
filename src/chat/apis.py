from fastapi import APIRouter, HTTPException, Request
import logging
from src.config import Config
from src.utils.logger import logger_set
import openai


router = APIRouter()

# Ensure the OpenAI API key is set
# OPENAI_API_KEY = Config.OPENAI_API_KEY
# if not OPENAI_API_KEY:
#     raise RuntimeError("OpenAI API key is not set. Please configure it.")

# Set the OpenAI API key
# openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(
    api_key=Config.OPENAI_API_KEY,  # This is the default and can be omitted
)


@router.post("")
async def ai_chat(request: Request, query: str, history: list[dict] = []):
    """
    Endpoint to interact with the ChatGPT model.

    Args:
        request (Request): The HTTP request object.
        query (str): The user's query to ChatGPT.
        history (list[dict]): The conversation history to provide context for the chat.

    Returns:
        dict: The AI-generated response.
    """
    try:
        # Log the incoming query
        logger_set.info(f"Received query: {query}")

        # Prepare the messages with conversation history
        messages = [{"role": "system", "content": "You are a helpful assistant."}] + history + [{"role": "user", "content": query}]

        # Call OpenAI's ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the desired model
            messages=messages
        )

        # Extract the AI's response
        ai_response = response.choices[0].message.content
        logger_set.info(f"AI response: {ai_response}")

        # Return the response to the user
        return {"query": query, "response": ai_response, "history": history + [{"role": "user", "content": query}, {"role": "assistant", "content": ai_response}]}

    except openai.OpenAIError as e:
        # Log the error
        logger_set.error(f"OpenAI API error: {e}")

        # Raise an HTTP exception with the error message
        raise HTTPException(status_code=500, detail="Error communicating with OpenAI API.")

    except Exception as e:
        # Log unexpected errors
        logger_set.error(f"Unexpected error: {e}")

        # Raise an HTTP exception with a generic error message
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
