import json
from services import save_user_on_db
from services import send_message_email_notifications_service


def default_callback(ch, method, properties, body):
    # TODO define router rules
    print('RECEIVE MESSAGE USER MICROSERVICE')
    payload = json.loads(body)
    print(" [x] Received %r" % payload)

    try:
        user_data = save_user_on_db(payload)
        send_message_email_notifications_service(user_data)
    except Exception as e:
        raise e