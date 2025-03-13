from myagents import run


def chat(q0, next_message, respond):
    history = []

    while True:
        if q0:
            q, q0 = q0, None
        else:
            try:
                q = next_message()
            except EOFError:
                return

        result = run(history, q)

        respond(result.final_output)

        history = result.to_input_list()
