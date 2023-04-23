def fix_stops(message):
    message = str(message)

    while ".." in message:
        message = message.replace("..", ",")

    return message.replace(")", ".").replace("!", ",").replace("*", " ").replace("_", " ")