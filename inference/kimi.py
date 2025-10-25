import openai
from .secret_key import rift_api_key

def chat_with_kimi(prompt, stream=True):
    """
    Send a prompt to the Kimi-K2-Instruct model and get a response.

    Args:
        prompt (str): The user message to send to the model
        stream (bool): Whether to stream the response (default: True)

    Returns:
        str: The complete response from the model (if stream=False)
        generator: A streaming response generator (if stream=True)
    """
    client = openai.OpenAI(
        api_key=rift_api_key,
        base_url="https://inference.cloudrift.ai/v1"
    )

    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=stream
    )

    if stream:
        return completion
    else:
        return completion.choices[0].message.content