from kbrainsdk.validation import get_payload

def validate_servicebus_message(req):
    body = get_payload(req)
    required_arguments = ["message", "topic_name", "application_properties"]

    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    message = body.get('message')
    topic_name = body.get('topic_name')
    application_properties = body.get('application_properties')    

    return message, topic_name, application_properties