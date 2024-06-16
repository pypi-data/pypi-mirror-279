import json
import logging
import os
import threading
import time

import requests
from requests import Timeout
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from doot.callback import BotCallback
from doot.command_handler import CommandHandler, DefaultCommandHandler
from doot.exception import CommandProcessingError, MessageProcessingError
from doot.message import Mapper, Update
from doot.message_handler import MessageHandler, DefaultMessageHandler
from doot.response import HandlerResponse


class Bot(BotCallback):

    def __init__(self, token: str):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__base_url = f'https://api.telegram.org/bot{token}'
        self.__send_msg_url = f'{self.__base_url}/sendMessage'
        self.__get_updates_url = f'{self.__base_url}/getUpdates'
        self.__send_photo_url = f'{self.__base_url}/sendPhoto'
        self.__send_doc_url = f'{self.__base_url}/sendDocument'
        self.__next_update_id = -1

        self.command_handler: CommandHandler = DefaultCommandHandler(self)
        self.message_handler: MessageHandler = DefaultMessageHandler(self)

    def _get_with_retries(self, url: str,
                          retries: int = 4,
                          backoff_factor: float =0.75,
                          status_forcelist=(429, 500, 502, 503, 504),
                          params = None,
                          data = None,
                          files = None,
                          timeout=5):
        """
        Make a GET request to a URL with retries.

        :param url: The URL to fetch.
        :param retries: Number of retries.
        :param backoff_factor: A backoff factor to apply between attempts after the second try.
        :param status_forcelist: A set of HTTP status codes that we should force a retry on.
        :return: Response object.
        """
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = None
        attempted = 0
        while attempted < retries:
            try:
                response = session.post(url, params=params, data=data, files=files, timeout=timeout)
                response.raise_for_status()  # Raise an HTTPError on bad responses
                break  # if code execution reached here means all went well.
            except Timeout as et:
                if attempted == retries:
                    raise et
                self.__logger.error(f"Error sending message > attempt {attempted+1}/{retries}: {et}")
            attempted = attempted + 1

        return response

    def send_notification(self, response: HandlerResponse, chat_id: int, disable_web_page_preview: bool = False):

        params = {
            'chat_id': chat_id,
            'text': response.get_message(),
            'parse_mode': response.get_message_parse_mode(),
            'disable_web_page_preview': str(disable_web_page_preview)
        }
        try:
            response = self._get_with_retries(self.__send_msg_url, params=params, timeout=5)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending message: {e}")
            raise e
        else:
            if response.status_code != 200:
                logging.error(f"Error: {response.text}")
            else:
                logging.info("Message sent successfully.")

    def send_photo(self, response: HandlerResponse, chat_id: int, disable_web_page_preview: bool = False):

        files = {
            'photo': open(response.get_photo_path(), 'rb'),
        }

        form_data = {
            'chat_id': chat_id,
            'caption': response.get_message(),
            'parse_mode': response.get_message_parse_mode(),
            'disable_web_page_preview': str(disable_web_page_preview)
        }
        try:
            response = self._get_with_retries(self.__send_photo_url, data=form_data, files=files, timeout=5)
            response.raise_for_status()  # Raise an error if response status code is not 200
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending message: {e}")
            raise e
        else:
            if response.status_code != 200:
                logging.error(f"Error: {response.text}")
            else:
                logging.info("Message sent successfully.")
        finally:
            files['photo'].close()

    def send_doc(self, response: HandlerResponse, chat_id: int, disable_web_page_preview: bool = False):

        files = {
            'document': open(response.get_document_path(), 'rb'),
        }

        form_data = {
            'chat_id': chat_id,
            'caption': response.get_message(),
            'parse_mode': response.get_message_parse_mode(),
            'disable_web_page_preview': str(disable_web_page_preview)
        }
        try:
            response = self._get_with_retries(self.__send_doc_url, data=form_data, files=files, timeout=5)
            response.raise_for_status()  # Raise an error if response status code is not 200
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending message: {e}")
            raise e
        else:
            if response.status_code != 200:
                logging.error(f"Error: {response.text}")
            else:
                logging.info("Message sent successfully.")
        finally:
            files['document'].close()

    def _fetch_updates(self):
        params = {
            'offset': self.__next_update_id
        }
        try:
            response = self._get_with_retries(self.__get_updates_url, params=params, timeout=5)
            response.raise_for_status()  # Raise an error if response status code is not 200
            resp_dict = json.loads(response.content)
            updates = Mapper().map(resp_dict['result'])
            if len(updates) > 0:
                self.__next_update_id = updates[len(updates) - 1].update_id + 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending message: {e}")
            raise e
        else:
            if response.status_code != 200:
                logging.error(f"Error: {response.text}")

        return updates

    def _process_command(self, update: Update):
        args = []
        for e in update.message.text.split(' '):
            if e != '':
                args.append(e)
        command = args.pop(0)

        response = None
        try:
            response = self.command_handler.handle_command(command, args, update.message.chat.id)
            self.respond(response, update)
        except Exception as e:
            raise CommandProcessingError(e)
        finally:
            self._delete_files_in_response(response)

    def _process_message(self, update: Update):
        response = None
        try:
            response = self.message_handler.handle_message(update.message.text, update.message.chat.id)
            self.respond(response, update)
        except Exception as e:
            raise MessageProcessingError(e)
        finally:
            self._delete_files_in_response(response)

    def respond(self, response: HandlerResponse, update: Update):
        if response.get_type() == 'text':
            self.send_notification(response, update.message.chat.id)
        elif response.get_type() == 'photo':
            self.send_photo(response, update.message.chat.id)
        elif response.get_type() == 'document':
            self.send_doc(response, update.message.chat.id)

    def interim_response(self, response: HandlerResponse, chat_id: int):
        try:
            if response.get_type() == 'text':
                self.send_notification(response, chat_id)
            elif response.get_type() == 'photo':
                self.send_photo(response, chat_id)
            elif response.get_type() == 'document':
                self.send_doc(response, chat_id)
        finally:
            self._delete_files_in_response(response)

    def _delete_files_in_response(self, response: HandlerResponse):
        if response is None:
            return

        if response.get_photo_path() is not None:
            try:
                os.remove(response.get_photo_path())
            except Exception as e:
                self.__logger.warning(f'Failed to delete file: {response.get_photo_path()}: {e}',
                                      stack_info=True, exc_info=True)

        if response.get_document_path() is not None:
            try:
                os.remove(response.get_document_path())
            except Exception as e:
                self.__logger.warning(f'Failed to delete file: {response.get_photo_path()}: {e}',
                                      stack_info=True, exc_info=True)

    def __drive(self, poll_delay: float):
        while True:
            try:

                updates = self._fetch_updates()
                for u in updates:
                    try:
                        if u.message.text is not None and u.message.text.startswith('/'):
                            self._process_command(u)
                        else:
                            self._process_message(u)
                    except MessageProcessingError as e:
                        self.__logger.error(f'Exception in processing update: {e}:\n{u}',
                                            stack_info=True, exc_info=True)
                        # just so we can move on
                        self.send_notification(HandlerResponse(message='Error in processing.'), u.message.chat.id)
                    time.sleep(poll_delay)

            except (ConnectionError, TimeoutError) as e:
                self.__logger.error(f'Error ==> {e}', stack_info=True, exc_info=True)
                time.sleep(15)  # To let systems recover
            except Exception as e:
                self.__logger.error(f'Error ==> {e}', stack_info=True, exc_info=True)

    def start(self, poll_delay: float = 5):
        my_thread = threading.Thread(target=self.__drive, args=[poll_delay])
        my_thread.start()


