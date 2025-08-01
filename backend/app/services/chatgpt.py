import os
import json
from dotenv import load_dotenv
from fastapi import HTTPException
from datetime import datetime, timezone
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError, OpenAIError

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("AI_API_KEY"),
)

class AIRequestError(Exception):
    """Base class for AI request errors."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def ask_chatgpt(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=os.getenv("AI_MODEL"),
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    
    except APIConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Connection error: {e}")
    
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {e}")
    
    except RateLimitError as e:
        try:
            body = json.loads(e.args[0])
            err = body.get("error", {})
            msg = err.get("message", "Request limit exceeded. Try again later.")
            meta = err.get("metadata", {})
            headers = meta.get("headers", {})

            # если есть заголовок сброса в миллисекундах
            reset_ms = headers.get("X-RateLimit-Reset")
            if reset_ms:
                reset_ts = datetime.fromtimestamp(int(reset_ms) / 1000, tz=timezone.utc)
                human = reset_ts.astimezone().strftime("%H:%M:%S")
                msg += f" Access will be restored in approximately {human}."
        except Exception:
            msg = "Request limit exceeded. Try again later."

        raise AIRequestError(msg, 429)
    
    except APIError as e:
        code = getattr(e, "status", None)
        body = ""
        try:
            body = json.loads(e.args[0])
            api_code = body.get("error", {}).get("code")
        except Exception:
            api_code = None

        if code == 408 or api_code == 408:
            raise AIRequestError("Timeout: The server did not have time to respond. Try again.", 408)
        if code == 502:
            raise AIRequestError("The service is temporarily unavailable. Try again later.", 502)
        
        msg = body.get("error", {}).get("message") if body else str(e)
        raise AIRequestError(f"AI service returned an error: {msg}", code or 500)
    
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
