class CPrint:

    @staticmethod
    def red(text: str):
        print(f"\033[91m {text}\033[00m")

    @staticmethod
    def green(text: str):
        print(f"\033[92m {text}\033[00m")

    @staticmethod
    def yellow(text: str):
        print(f"\033[93m {text}\033[00m")

    @staticmethod
    def blurple(text: str):
        print(f"\033[94m {text}\033[00m")

    @staticmethod
    def purple(text: str):
        print(f"\033[95m {text}\033[00m")

    @staticmethod
    def cyan(text: str):
        print(f"\033[96m {text}\033[00m")

    @staticmethod
    def gray(text: str):
        print(f"\033[97m {text}\033[00m")

    @staticmethod
    def black(text: str):
        print(f"\033[98m {text}\033[00m")
