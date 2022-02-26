class Logger:
    @staticmethod
    def error(code: int):
        print("Exited @ {code}".format(code=code))
        exit(code)
