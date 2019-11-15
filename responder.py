import time
import random
import re
import giphy_client
import json

from fbchat import Client, log
from fbchat.models import Message
from giphy_client.rest import ApiException
from local_settings import EMAIL, PASSWORD, API_KEY, NOT_FOUND, cookies
from local_settings import JJ_GIF, JJ_MSG, RESP_LIST, USERS


class ResponseBot(Client):
    # TODO: clean the motherfucking code
    def onMessage(self,
                  author_id,
                  message_object,
                  thread_id,
                  thread_type,
                  **kwargs):
        msg = ''
        gif_url = ''

        if message_object.text is not None:
            msg = message_object.text.lower()
            # def status
            if "@gif_bot komendy" in msg:
                self.send(Message(text=('1) @gif ___\n'
                                        '2) @julia\n'
                                        '3) {}').format(RESP_LIST)),
                          thread_id=thread_id,
                          thread_type=thread_type)
            # def julia
            if re.search("^@julia.*", msg.lower()):
                self.sendRemoteFiles([JJ_GIF],
                                     Message(text=JJ_MSG),
                                     thread_id=thread_id,
                                     thread_type=thread_type)
                log.warning("-----HEHE XD-----")
            if author_id in USERS[0:3]:
                # def auto_reply
                for resp in RESP_LIST:
                    if resp in msg:
                        response = resp
                        if response is not None:
                            log.warning("-----AUTO-REPLY----- => ({})"
                                        .format(response))
                            time.sleep(2)
                            self.markAsRead(thread_id)
                            self.markAsDelivered(thread_id, message_object.uid)
                            time.sleep(1)
                            self.send(Message(text=response),
                                      thread_id=thread_id,
                                      thread_type=thread_type)
            # def is_gif
            if ((author_id in USERS or author_id == self.uid)
                    and re.search("^@gif .*", msg)):

                query = re.sub("^@gif ", '', msg)
                gif_num = random.randint(1, 20)
                # def search_gif
                try:
                    api_response = api_instance.gifs_search_get(
                        API_KEY, query)

                    json_data = None
                    if api_response.data is not None:

                        json_data = api_response.data
                        # def validate_
                        if len(json_data) > gif_num:
                            gif_url = json_data[gif_num].images.downsized.url
                            self.sendRemoteFiles([gif_url],
                                                 Message(text="<3"),
                                                 thread_id=thread_id,
                                                 thread_type=thread_type)
                            log.warning('SEND [{}] OF => ({})'
                                        .format(gif_num, query))

                        elif len(json_data) > 0:

                            gif_url = json_data[0].images.downsized.url
                            self.sendRemoteFiles([gif_url],
                                                 Message(
                                                 text=";*"),
                                                 thread_id=thread_id,
                                                 thread_type=thread_type)
                            log.warning('SEND [0] OF => ({})'
                                        .format(query))

                        else:
                            self.send(Message(
                                      text=NOT_FOUND),
                                      thread_id=thread_id,
                                      thread_type=thread_type)
                            log.warning('NOT FOUND => {}'
                                        .format(query))

                except ApiException as e:
                    log.warning('''Exception when calling DefaultApi->
                                    gifs_search_get: {}'''
                                .format(e))


api_instance = giphy_client.DefaultApi()

client = ResponseBot(EMAIL, PASSWORD, None, 5, cookies, 30)

with open('cookies.json', 'w') as fd:
    cookies = client.getSession()
    json.dump(cookies, fd)

client.listen()
