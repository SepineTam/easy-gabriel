from datetime import datetime
from pathlib import Path
from typing import Callable, List, Literal

import gabriel as openai_gabriel
import pandas as pd

from openai_api_polling.polling import APIPolling, ClientPolling


class EasyGABRIEL:
    """Current is based on openai-gabriel v1.1.1"""

    SUPPORTED_METHODS = {
        'rate', 'classify', 'extract', 'deidentify', 'rank', 'codify',
        'paraphrase', 'compare', 'discover', 'deduplicate', 'merge',
        'filter', 'debias', 'ideate', 'id8', 'whatever', 'view',
        'bucket', 'seed',
    }

    def __init__(
        self, 
        *,
        api_polling: APIPolling,
        base_url: str, 
        model: str, 
        response: Literal["openai"] = "openai",
        save_dir_base: Path | str = None,
    ):
        self.client_polling = ClientPolling(api_polling)
        self.base_url = base_url
        self.model = model
        self.response_fn = response_fn_generator(
            client_polling=self.client_polling,
            response=response
        )

        self.save_dir_base = Path(
            save_dir_base or Path.cwd() / "easy_gabriel_outputs"
        )

    def update_kwargs(self, **kwargs) -> dict:
        if "model" not in kwargs:
            kwargs["model"] = self.model
        if "save_dir" not in kwargs:
            signature = datetime.now().strftime("%Y%m%d_%H%M%S")
            kwargs["save_dir"] = self.save_dir_base / signature
        kwargs["response_fn"] = self.response_fn
        return kwargs

    def __getattr__(self, name):
        if name not in self.SUPPORTED_METHODS:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        func = getattr(openai_gabriel, name)
        async def wrapper(*args, **kwargs):
            kwargs = self.update_kwargs(**kwargs)
            return await func(*args, **kwargs)
        return wrapper


def response_fn_generator(
    client_polling: ClientPolling, 
    response: Literal["openai"] = "openai"
) -> Callable:
    async def openai_response(
        prompt: str,
        *,
        model: str = None,
        json_mode: bool = False,
        **kwargs
    ) -> str: 
        messages = [
            {"role": "user", "content": prompt}
        ]
        params = {
            "model": model,
            "messages": messages,
        }

        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        response = await client_polling.async_client.chat.completions.create(**params)
        return response.choices[0].message.content

    if response == "openai":
        return openai_response
    else:
        raise ValueError("Invalid response type. Must in ['openai'].")

def init_gabriel(
    api_key: str | List | APIPolling = None, 
    base_url: str = "https://api.deepseek.com/v1",
    model: str = "deepseek-chat", 
    response: Literal["openai"] = "openai",
    save_dir_base: Path | str = None,
) -> EasyGABRIEL:
    if isinstance(api_key, str):
        api_polling = APIPolling([api_key])
    elif isinstance(api_key, List):
        api_polling = APIPolling(api_key)
    elif isinstance(api_key, APIPolling):
        api_polling = api_key
    elif api_key is None:
        api_polling = APIPolling.load_api()
    else:
        raise ValueError("Invalid api_key type. Must be str, List, APIPolling, or None.")

    if response not in ["openai"]:
        raise ValueError("Invalid response type. Must be 'openai'.")

    return EasyGABRIEL(
        api_polling=api_polling, 
        base_url=base_url, 
        model=model, 
        response=response, 
        save_dir_base=save_dir_base
    )
