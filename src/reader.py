from message_factory import MessageFactory


def read_itch(file_path):

    with open(file_path, 'rb') as data:
        while True:
            message_size = int.from_bytes(data.read(2), byteorder='big', signed=False)
            message_type = data.read(1).decode('ascii')
            record = data.read(message_size - 1)
            message = MessageFactory.create_message(message_type, record)
            message.register()
