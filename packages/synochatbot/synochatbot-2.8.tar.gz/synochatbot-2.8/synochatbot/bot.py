import requests
from flask import Flask, request
import time
import threading
import os
#from .__init__ import outgoing_webhook_global
import queue

app = Flask(__name__)

# Replace <incoming_webhook_url> with your incoming webhook URL
incoming_webhook_url = "redacted for privacy"

message_queue = queue.Queue()

def send_message(message, outgoing_webhook, attachment_text=None):
 if attachment_text is None:
    encoded_message = message.encode('utf-8')
    payload = f'payload={{"text": "{encoded_message.decode("latin-1")}"}}'
    response = requests.post(outgoing_webhook, data=payload)
    return response.status_code == 200
 else:
    encoded_message = message.encode('utf-8')
    payload = f'payload={{"text": "{message}", "attachments": [{{"callback_id": "abc", "text": "{attachment_text}", "actions": [{{"type": "button", "name": "resp", "value": "ok", "text": "OK", "style": "green"}}]}}]}}'

    if message != 'Bot: Message sent successfully!':
      response = requests.post(outgoing_webhook, data=payload)
      return response.status_code == 200

@app.route("/", methods=["GET", "POST"])
def receive_message():
    if request.method == 'POST':
        if request.form.get("token") == incoming_webhook_url1:
            message = request.form["text"]
            username = request.form["username"]
            response = f"The message {message} has not been defined."

            parts = message.split(" ")
            if len(parts) > 0:
                alias = parts[0].lower()

                # Put the message into the queue
                message_queue.put((alias, message, username))

                response = "Bot: Message received successfully."
            else:
                response = "Error: Invalid message format."

            print("Message: '" + message + "' has been sent by " + username)
            return response
        else:
            return "Authentication Error", 401
    else:
        return "hello"

def start_flask_app(port):
    app.run(host='0.0.0.0', port=port)

def process_messages(instance, outgoing_webhook, incoming_webhook_url):
    global incoming_webhook_url1
    incoming_webhook_url1 = incoming_webhook_url
    while True:
        try:
            alias, message, username = message_queue.get(block=True, timeout=1)
            class Message1:
                def __init__(self, content, username):
                    self.content = content
                    self.username = username
    
                def __str__(self):
                    return self.content
    
            msg = Message1(message, username)
            
            # Process the message here
            if alias in instance.alias_to_func:
                func = instance.alias_to_func[alias]
                parts = msg.content.split(" ")
                if len(parts) > 1:
                    arg_str = " ".join(parts[1:])
                    arg_parts = arg_str.split(":::")
                    response = func(msg, *arg_parts)
                    if response:
                        send_message(str(response), outgoing_webhook)
                else:
                    response = func(msg)
                    if response:
                        send_message(str(response), outgoing_webhook)
            else:
                print(f"Unknown alias: {alias}")
        except queue.Empty:
            # No messages in the queue, wait for the next one
            pass

def run_bot(instance, outgoing_webhook, incomming_token, port):
    flask_thread = threading.Thread(target=start_flask_app, args=(port,))
    message_thread = threading.Thread(target=process_messages, args=(instance, outgoing_webhook, incomming_token))
    flask_thread.start()
    message_thread.start()