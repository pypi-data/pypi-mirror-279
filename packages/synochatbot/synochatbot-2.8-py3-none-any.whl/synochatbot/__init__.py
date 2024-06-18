#from .instance import instance
from .bot import app, send_message, run_bot
import threading
import time
time.sleep(1)

class SynoBot:
    def __init__(self):
        self.alias_to_func = {}
        self.on_unknown_message1 = False

    def message(self, alias, arguments=0):
        def decorator(func):
            self.alias_to_func[alias] = func
            return func
        return decorator
    
    def on_unknown_message(self, func):
        def wrapper(*args, **kwargs):
            # Code to handle unknown messages goes here
            print("Unknown message.")
            self.on_unknown_message1 = True
        
            # Call the original function
            return func(*args, **kwargs)
    
        return wrapper

    def run(self, **kwargs):
        flask_thread = threading.Thread(target=app.run, kwargs=kwargs)
        flask_thread.start()
def instance():
    return SynoBot()