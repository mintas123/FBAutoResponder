# Auto-reply and send gifs in Facebook Messenger


## Installation

```bash
pip install fbchat
pip install giphy_client
```
## Usage
To run you need to create local_settings.py file, containing the imported constants.

```python
API_KEY = # Your giphy api key
EMAIL = # FB credentials
PASSWORD = # FB credentials

USERS = [] # contains users you want to reply to

RESP_LIST = [] # contains regex of words/ sentences you want to auto-reply to
NOT_FOUND = # message when searched gif is not found

```
