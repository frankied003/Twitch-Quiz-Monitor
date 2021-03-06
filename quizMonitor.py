import os
from dotenv import load_dotenv
import socket
import logging
from emoji import demojize
import re

# loading environment variables
load_dotenv()


class bcolors:
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# variables for socket
server = "irc.chat.twitch.tv"
port = 6667
nickname = "frankied003"
token = os.getenv("TWITCH_TOKEN")
channel = "#xqcow"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d — %(message)s",
    datefmt="%Y-%m-%d_%H:%M:%S",
    handlers=[logging.FileHandler("chat.log", encoding="utf-8")],
)

# creating the socket and connecting
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode("utf-8"))
sock.send(f"NICK {nickname}\n".encode("utf-8"))
sock.send(f"JOIN {channel}\n".encode("utf-8"))

while True:
    consoleInput = input(
        "Enter correct answer to the question (use a ',' for multiple answers):"
    )

    # if console input is stop, the code will stop ofcourse lol
    if consoleInput == "stop":
        break

    # make array of all the correct answers
    correctAnswers = consoleInput.split(",")
    correctAnswers = [answer.strip().lower() for answer in correctAnswers]

    correctAnswerFound = False

    # while the correct answer is not found, the chats will keep on printing
    while correctAnswerFound is not True:

        while True:
            try:
                resp = sock.recv(2048).decode("utf-8")
            except:
                continue
            break

        if resp.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))

        elif len(resp) > 0:
            # some responses have mulitple messages, split them
            for response in resp.split("\n\n"):
                messagesInResponse = response.strip().splitlines()
                for twitchMessage in messagesInResponse:

                    # only happens after I connect so I need this here to keep it going
                    try:
                        username = twitchMessage.split(":")[1].split("!")[0]
                        message = twitchMessage.split(":")[2]
                    except:
                        break

                    strippedMessage = " ".join(message.split())  # remove white space
                    logMessage = username + " - " + message
                    logging.info(demojize(logMessage))  # for emojis

                    # once the answer is found, the chats will stop, correct answer is highlighted in green, and onto next question
                    if str(strippedMessage).lower() in correctAnswers:
                        print(
                            bcolors.OKGREEN + username + " - " + message + bcolors.ENDC
                        )
                        correctAnswerFound = True
                        break
                    else:
                        if username == nickname:
                            print(
                                bcolors.OKCYAN
                                + username
                                + " - "
                                + message
                                + bcolors.ENDC
                            )
                        else:
                            print(username + " - " + message)
