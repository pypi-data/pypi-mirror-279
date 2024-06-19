import time
import tiktoken
from openai import OpenAI
from typing import Dict

def count_tokens_in_string(text: str) -> int:
    """
    Counts the number of tokens in a given string using the tiktoken library.

    Args:
    text (str): The text to be tokenized.

    Returns:
    int: The number of tokens in the text.
    """
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception as e:
        print(f"Error in count_tokens_in_string, text input: {text}, error: {e}")
        return 0

def llm_performance_benchmark(model_id: str, 
                              user_prompt: str, 
                              system_prompt: str, 
                              api_key: str, 
                              base_url: str = "https://api.openai.com/v1", 
                              max_tokens: int = 500, 
                              temperature: float = 0.2, 
                              print_response: bool = False) -> Dict[str, float]:
    """
    Benchmarks the performance of OpenAI compatible APIs.

    Args:
    model_id (str): The model identifier per the host provider
    user_prompt (str): Input prompt
    system_prompt (str): System prompt
    api_key (str): The API key for authentication.
    base_url (str): The base URL of the API endpoint. Defaults to "https://api.openai.com/v1".
    max_tokens (int): The maximum number of tokens to generate. Defaults to 500.
    temperature (float): Model temperature. Defaults to 0.2.
    print_response (bool): Whether to log the response. Defaults to False.

    Returns:
        Dict[str, float]: A dictionary with benchmarking metrics where:
            'total_time' (float)
            'time_to_first_token' (float)
            'tokens_per_second' (float)
            'tokens_per_second_across_total_request' (float)
            'response_text' (str)
     """

    openai_client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    start_time = time.time()
    first_token_time = None
    first_chunk_tokens = None
    first_chunk_content = None
    full_response_string = ''
    all_chunks = []

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    for response in openai_client.chat.completions.create(
        model=model_id, 
        messages=messages, 
        stream=True,
        temperature=temperature, 
        max_tokens=max_tokens):

        chunk_content = response.choices[0].delta.content if hasattr(response.choices[0].delta, 'content') else response.choices[0].delta

        if first_token_time is None:
            first_token_time = time.time()
            first_chunk_content = chunk_content
        if chunk_content != "" and isinstance(chunk_content, str):
            full_response_string += chunk_content
            all_chunks.append(chunk_content)

        if print_response:
            print(chunk_content)

    if print_response:
        print("Complete response:")
        print(full_response_string)

    end_time = time.time()
    total_time = end_time - start_time
    time_to_first_token = first_token_time - start_time

    first_chunk_tokens = count_tokens_in_string(first_chunk_content)
    completion_tokens = count_tokens_in_string(full_response_string)

    outputting_time_after_first_chunk = end_time - first_token_time
    tokens_excl_first_chunk = completion_tokens - first_chunk_tokens
    tps_excl_first_chunk = tokens_excl_first_chunk / outputting_time_after_first_chunk

    tokens_per_second_across_total_request = completion_tokens / total_time

    return_dict = {
        "total_time": total_time,
        "time_to_first_token": time_to_first_token,
        "output_tokens_per_second": tps_excl_first_chunk,
        "tokens_per_second_across_total_request": tokens_per_second_across_total_request,
        "response_text": full_response_string
    }

    return return_dict
