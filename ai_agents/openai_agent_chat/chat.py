"""Common code to chat with the agent."""

from myagents import run


def chat(q0, next_message, respond):
    """Chat with the agent.

    Args:
        q0: The initial input to the agent.
        next_message: A function that returns the next message from the user.
        respond: A function that sends a message to the user.
    """
    history = []

    while True:
        if q0:
            q, q0 = q0, None
        else:
            try:
                q = next_message()
            except EOFError:
                respond("Goodbye!")
                return

        result = run(history, q)

        respond(result.final_output)

        history = result.to_input_list()
