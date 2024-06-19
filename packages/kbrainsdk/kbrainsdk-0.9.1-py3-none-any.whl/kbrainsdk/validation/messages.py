from kbrainsdk.validation.common import get_payload

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

def validate_servicebus_topic(req):
    body = get_payload(req)
    required_arguments = ["topic_name"]

    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    topic_name = body.get('topic_name')

    return topic_name

def validate_servicebus_queue(req):
    body = get_payload(req)
    required_arguments = ["queue_name"]

    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    queue_name = body.get('queue_name')

    return queue_name

def validate_create_subscription(req):

    body = get_payload(req)
    required_arguments = ["topic_name", "subscription_name"]

    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))
    
    topic_name = body.get('topic_name')
    subscription_name = body.get('subscription_name')
    max_delivery_count = body.get('max_delivery_count', 10)
    default_message_time_to_live = body.get('default_message_time_to_live', "P14D")
    lock_duration = body.get('lock_duration', "PT1M")
    requires_session = body.get('requires_session', False)
    dead_lettering_on_message_expiration = body.get('dead_lettering_on_message_expiration', True)
    dead_lettering_on_filter_evaluation_exceptions = body.get('dead_lettering_on_filter_evaluation_exceptions', True)
    forward_to = body.get('forward_to', None)
    forward_dead_lettered_messages_to = body.get('forward_dead_lettered_messages_to', None)
    enable_batched_operations = body.get('enable_batched_operations', True)
    status = body.get('status', "active")

    return topic_name, subscription_name, max_delivery_count, default_message_time_to_live, \
        lock_duration, requires_session, dead_lettering_on_message_expiration, dead_lettering_on_filter_evaluation_exceptions, \
            forward_to, forward_dead_lettered_messages_to, enable_batched_operations, status


def validate_send_signalr(req):
    body = get_payload(req)
    required_arguments = ["message", "target", "hub_name"]

    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    message = body.get('message')
    target = body.get('target')
    hub_name = body.get('hub_name')
    group_name = body.get('group_name', None)

    return message, target, hub_name, group_name

def validate_create_signalr_hub(req):
    body = get_payload(req)
    required_arguments = ["hub_name"]

    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    hub_name = body.get('hub_name')

    return hub_name
