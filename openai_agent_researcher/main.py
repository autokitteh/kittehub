from chat import chat


def main():
    def next_message():
        return input("Q: ")

    def respond(txt):
        print(f"A: {txt}")

    chat(None, next_message, respond)


if __name__ == "__main__":
    main()
