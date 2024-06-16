

class MessageProcessingError(RuntimeError):

    def __init__(self, *args):
        super().__init__(*args)


class CommandProcessingError(MessageProcessingError):

    def __init__(self, *args):
        super().__init__(*args)


