
from kbrainsdk.validation.common import get_payload
import re

common_arguments = [
    "model_name", "model_type", 
    "temperature", "max_tokens", "base_url", "deployment_id", "full_response", 
    "max_tokens", "frequency_penalty", "presence_penalty", "stop", "n", 
    "stream", "logit_bias", "response_format", "best_of", 
    "seed", "tools", "tool_choice"
]
common_required_arguments = ["model_name", "model_type", "deployment_id"]

chat_arguments = ["messages"] + common_arguments
chat_required_arguments = ["messages"] + common_required_arguments
completion_arguments = ["prompt"] + common_arguments
completion_required_arguments = ["prompt"] + common_required_arguments

ENDPOINT_TYPES = {
    "chat": {
        "arguments": chat_arguments,
        "required_arguments": chat_required_arguments
    },
    "completion": {
        "arguments": completion_arguments,
        "required_arguments": completion_required_arguments
    }
}


def validate_aistudio_llms(req, endpoint_type):
    payload = get_payload(req)
    arguments = ENDPOINT_TYPES[endpoint_type]["arguments"]
    required_arguments = ENDPOINT_TYPES[endpoint_type]["required_arguments"]
    # Create log_payload, excluding keys with None values
    log_payload = {key: payload[key] for key in arguments if (key in payload and payload[key] is not None)}

    # Check if mandatory values are present
    missing_values = [value for value in required_arguments if value not in log_payload]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    return log_payload


def validate_openai_llms(req, endpoint_type):    
    return validate_aistudio_llms(req, endpoint_type)

def extract_integer(x, default):
    match = re.search(r'\d+', x)
    if match:
        return int(match.group())
    else:
        return default