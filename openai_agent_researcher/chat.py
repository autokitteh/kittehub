from myagents import run


def chat(next_message, respond):
    history = []

    while True:
        try:
            q = next_message()
        except EOFError:
            return

        result = run(history, q)

        respond(result.final_output)

        history = result.to_input_list()
