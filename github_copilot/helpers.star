load("@github", "mygithub")
load("@slack", "myslack")

def _email_to_slack_user_id(email):
    resp = myslack.users_lookup_by_email(email)
    return resp.user.id if resp.ok else ""

def github_username_to_slack_user_id(github_username, github_owner_org):
    resp = mygithub.get_user(github_username, owner = github_owner_org)
    github_user_link = "<%s|%s>" % (resp.htmlurl, github_username)

    if resp.type == "Bot":
        return ""

    # Try to match by the email address first.
    if resp.email:
        slack_user_id = _email_to_slack_user_id(resp.email)
        if slack_user_id:
            return slack_user_id

    # Otherwise, try to match by the user's full name.
    if not resp.name:
        return ""

    gh_full_name = resp.name.lower()
    for user in _slack_users():
        slack_names = (user.profile.real_name.lower(), user.profile.real_name_normalized.lower())
        if gh_full_name in slack_names:
            return user.id

    return ""

def _slack_users(cursor = ""):
    resp = myslack.users_list(cursor, limit = 100)
    if not resp.ok:
        return []

    users = resp.members
    if resp.response_metadata.next_cursor:
        users += _slack_users(resp.response_metadata.next_cursor)
    return users
