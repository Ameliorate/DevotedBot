from devbot.exception import ChatMessageTooLongError


def say(message, protocol):
    if len(message) >= 100:
        raise ChatMessageTooLongError
    protocol.send_packet("chat_message", protocol.buff_type.pack_string(message))