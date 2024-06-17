from . import config
import openai
import streamlit as st

# Define required environment variables
REQUIRED_VARS = [
    "AZURE_BASE_URL", "AZURE_API_KEY", "AZURE_DEPLOYMENT_VERSION", "AZURE_DEPLOYMENT_NAME"
]

# Load and validate environment variables
env_vars = config.load_and_validate_env_vars(REQUIRED_VARS)

# Azure API details
GPT_4o_CONTEXT_WINDOW = 128000

@st.cache_resource
def load_azure_client(
    base_url=env_vars["AZURE_BASE_URL"], 
    version=env_vars["AZURE_DEPLOYMENT_VERSION"], 
    api_key=env_vars["AZURE_API_KEY"]
):
    """
    Loads and caches the Azure OpenAI client.

    Returns:
        openai.AzureOpenAI: An instance of the Azure OpenAI client.
    """
    return openai.AzureOpenAI(
        azure_endpoint=base_url,
        api_version=version,
        api_key=api_key
    )

def query_llm(client, prompt, model_type, max_tokens=4096, temperature=0.0, seed = None):
    """
    Queries the Azure OpenAI language model with the given prompt.

    Args:
        config (dict): A dictionary containing the configuration details.
        prompt (str): The prompt to send to the language model.
        model_type (str): The deployment name in your Azure model deployments.
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 4096.
        temperature (float, optional): The sampling temperature. Defaults to 0.0.

    Returns:
        dict: The response from the language model.
    """
    response = client.chat.completions.create(
        model=model_type,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        seed = seed
    )
    return response

def get_content(response_full):
    return response_full.choices[0].message.content

def get_token_usage(response_full):
    return response_full.usage.total_tokens