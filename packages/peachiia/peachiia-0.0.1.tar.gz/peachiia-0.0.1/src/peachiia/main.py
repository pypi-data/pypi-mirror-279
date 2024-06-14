from utils.dummy import dummy_message
# helpy() will be accessible from this file but not from package level


def hello():
    print("Hello from Peachiia's Package! :P")


def help():
    print("Peachiia Package V.0.0.1")
    print("  Help : (not implemented yet, :P)")
    dummy_message()


if __name__ == "__main__":
    hello()