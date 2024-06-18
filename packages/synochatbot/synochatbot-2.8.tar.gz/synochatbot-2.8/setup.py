from setuptools import setup, find_packages

setup(
    name='synochatbot',
    version='2.8',
    author='kokofixcomputers',
    description='A discord.py like thing but for synology chat',
    long_description_content_type='text/markdown',
    long_description='''
# A python library like discord.py but for synology chat.

It allows you to create a bot that can be used to respond to messages in synology chat.

## Install:
``pip install synochatbot``

## Usage:
```python
import synochatbot as synochat

outgoing_webhook = "your url"
instance = synochat.instance()

@instance.message(alias="return_full_message")
def say_hi(message):
    return message

@instance.message(alias='return_username')
def return_test(message, command=None):
    return message.username

@instance.message(alias='arguments', arguments=5) #can have unlimited arguments
def return_test(message, arg1, arg2, arg3, arg4, arg5):
    return arg1 + arg2 + arg3 + arg4 + arg5

# ... (other message handlers)

synochat.run_bot(instance, outgoing_webhook, incomming_webhook_token)
```
Post arguments like this:
arguments arg1data:::arg2data:::arg3data:::arg4data:::arg5data
    ''',
    packages=find_packages(),
    install_requires=[
        'flask==3.0.3',
        'requests==2.31.0'
    ],
)
