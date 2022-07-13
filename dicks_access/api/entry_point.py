from message_factory import MessageFactory
from utils import get_message_recipients

if __name__ == "__main__":
    message_type = input("Please enter message type(Hint: Birthdays): ")

    factory = MessageFactory()
    factory_obj = factory.get_message(message_type)

    data = get_message_recipients()
    message = factory_obj.message(data)

    print(message)