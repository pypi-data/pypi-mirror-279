import os


class HandlerResponse:

    def __init__(self, message: str = None, photo_path: str = None, document_path: str = None, message_parse_mode: str = 'HTML'):
        self.__message = message
        self.__message_parse_mode = message_parse_mode
        self.__photo_path = photo_path
        self.__document_path = document_path

        if self.__photo_path is not None and not os.path.exists(self.__photo_path):
            raise RuntimeError(f'Attempt to set invalid photo to response: {photo_path}')

        if self.__document_path is not None and not os.path.exists(self.__document_path):
            raise RuntimeError(f'Attempt to set invalid photo to response: {photo_path}')

    def set_message(self, message: str):
        self.__message = message

    def get_message(self):
        return self.__message

    def set_message_parse_mode(self, message_parse_mode: str):
        self.__message_parse_mode = message_parse_mode

    def get_message_parse_mode(self):
        return self.__message_parse_mode

    def set_photo_path(self, photo_path: str):
        if self.__document_path is not None:
            raise RuntimeError('Attempt to set photo to response which already has a document')
        if not os.path.exists(photo_path):
            raise RuntimeError(f'Attempt to set invalid photo to response: {photo_path}')
        self.__photo_path = photo_path

    def get_photo_path(self):
        return self.__photo_path

    def set_document_path(self, doc_path: str):
        if self.__photo_path is not None:
            raise RuntimeError('Attempt to set document to response which already has a photo')

        if not os.path.exists(doc_path):
            raise RuntimeError(f'Attempt to set invalid document to response: {doc_path}')

        self.__document_path = doc_path

    def get_document_path(self):
        return self.__document_path

    def get_type(self):
        if self.__photo_path is None and self.__document_path is None:
            return 'text'
        elif self.__photo_path is not None and self.__document_path is None:
            return 'photo'
        elif self.__photo_path is None and self.__document_path is not None:
            return 'document'
        else:
            raise RuntimeError(f'Illegal state: {self.__repr__()}')

    def __repr__(self):
        return (f'HandlerResponse( message={self.__message}, message_parse_mode={self.__message_parse_mode}, '
                f'photo_path={self.__photo_path}, document_path={self.__document_path})')




