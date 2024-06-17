from colorama import Fore

red = Fore.RED
blue = Fore.BLUE
cyan = Fore.CYAN
green = Fore.GREEN
light_magenta = Fore.LIGHTMAGENTA_EX
green = Fore.GREEN
reset = Fore.RESET



class ResponseNotOK(BaseException):
    def __init__(self, response_text):
        self.response_text = response_text

    def send_message(self):
        return (
            red
            + f"[ERROR]"
            + reset
            + f"The API encountered an error:\n {self.response_text}"
        )


class PlayerNotFound(BaseException):
    def __int__(self, response_text):
        self.response_text = response_text

    def send_message(self):
        return (
            red + f"[ERROR]" + reset + f"The user is not found:\n {self.response_text}"
        )


class NoNetwork(BaseException):

    def send_message():
        return print (
            red
            + f"[ERROR]    "
            + "Can not reach API. Please make sure you are connected to a network."
        )
