import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    is_bot: bool
    language_code: str
    first_name: str = 'NA'
    last_name: str = 'NA'
    username: str = 'NA'


@dataclass
class Chat:
    id: int
    type: str
    first_name: str = 'NA'
    last_name: str = 'NA'
    username: str = 'NA'


@dataclass
class Message:
    message_id: int
    from_user: User
    chat: Chat
    text: str
    date: str

    def __post_init__(self):
        self.date = datetime.fromtimestamp(self.date).strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class Update:
    update_id: int
    message: Message


class Mapper:

    def map(self, data_dict: dict):

        updates = []
        for update_dict in data_dict:

            msg_dict = update_dict.get('message')
            from_user = User(**msg_dict['from'])
            if msg_dict.get('chat') is not None:
                chat = Chat(**msg_dict.get('chat'))

                # Create Message object
                message = Message(message_id=msg_dict['message_id'],
                                  from_user=from_user,
                                  chat=chat,
                                  date=msg_dict['date'],
                                  text=msg_dict.get('text'))

                updates.append(Update(update_id=update_dict['update_id'], message=message))

        return updates



if __name__ == '__main__':
    # Sample JSON data
    json_data = '''
        {
            "ok": true,
            "result": [
                {
                    "update_id": 300080505,
                    "message": {
                        "message_id": 527,
                        "from": {
                            "id": 6247567702,
                            "is_bot": false,
                            "first_name": "Amit Kumar Sharma",
                            "language_code": "en"
                        },
                        "chat": {
                            "id": 6247567702,
                            "first_name": "Amit Kumar Sharma",
                            "type": "private"
                        },
                        "date": 1715326007,
                        "text": "hello"
                    }
                },
                {
                    "update_id": 300080506,
                    "message": {
                        "message_id": 528,
                        "from": {
                            "id": 6247567702,
                            "is_bot": false,
                            "first_name": "Amit Kumar Sharma",
                            "username": "amit_9b",
                            "language_code": "en"
                        },
                        "chat": {
                            "id": 6247567702,
                            "first_name": "Amit Kumar Sharma",
                            "username": "amit_9b",
                            "type": "private"
                        },
                        "date": 1715326007,
                        "text": "world"
                    }
                },
                {
                    "update_id": 300080507,
                    "message": {
                        "message_id": 529,
                        "from": {
                            "id": 6247567702,
                            "is_bot": false,
                            "first_name": "Amit Kumar Sharma",
                            "username": "amit_9b",
                            "language_code": "en"
                        },
                        "chat": {
                            "id": 6247567702,
                            "first_name": "Amit Kumar Sharma",
                            "username": "amit_9b",
                            "type": "private"
                        },
                        "date": 1715326008,
                        "text": "whatsup"
                    }
                }
            ]
        }
    '''
    # Convert JSON to a dictionary
    data_dict = json.loads(json_data)
    updates = Mapper().map(data_dict['result'])
    # Access Message attributes
    print(updates)
