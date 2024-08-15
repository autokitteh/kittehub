import autokitteh


def on_cross_repo(event):
    print("This is a cross-repo action")
    s = autokitteh.subscribe("github_connection", "data.action == 'completed'")
    e = autokitteh.next_event(s)
    print(e)
