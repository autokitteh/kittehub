import datetime
import time

import autokitteh
from autokitteh import github, google


g = github.github_client("github_conn")
sheets = google.google_sheets_client("googlesheets_conn")


def on_start(_):
    # TODO: set up trigger based on slack mention
    # get sheets data and create a set of comment IDs
    comment_ids = get_sheets_data(
        "1kl6Y9vLOx6JDjcDqhEiigcnyLbzdW4avdSa4NOdegx4", "Sheet1"
    )
    comment_ids_set = set()
    for row in comment_ids["values"]:
        comment_ids_set.add(row[0])

    while True:
        get_github_comments(comment_ids_set)
        time.sleep(300)


def get_github_comments(comment_ids_set: set):
    print(f"comment_ids_set: {comment_ids_set}")
    # get all comments where the user hasn't responded in over 24 hours
    repo = g.get_repo("autokitteh/autokitteh")

    # Get all open PRs
    pulls = repo.get_pulls(state="open")

    unresponded = []

    # Process each pull request
    for pr in pulls:
        issue_comments = list(pr.get_issue_comments())
        inline_comments = list(pr.get_comments())
        now = datetime.datetime.now(datetime.UTC)
        process_issue_comments(issue_comments, now, comment_ids_set, unresponded)
        process_inline_comments(inline_comments, now, comment_ids_set, unresponded)

    print(f"unresponded list: {unresponded}")
    # Print results
    for comment_id, author, body, url in unresponded:
        print(f"PR #{comment_id} - Comment by {author}: {body}\nURL: {url}\n")
        append_row_to_sheet(
            "1kl6Y9vLOx6JDjcDqhEiigcnyLbzdW4avdSa4NOdegx4", "Sheet1", unresponded
        )


def process_issue_comments(issue_comments, now, comment_ids_set, unresponded):
    # Process issue comments (PR discussion)
    for comment in issue_comments:
        # TODO: need to do a slack lookup for the user
        if comment.user.login == "pashafateev":
            continue
        if "pashafateev" in comment.body:
            # Only consider if the comment is older than 24 hours
            if now - comment.created_at < datetime.timedelta(hours=24):
                continue
            responded = False
            # Check if an emoji reaction from pashafateev exists
            for reaction in comment.get_reactions():
                if reaction.user.login == "pashafateev":
                    responded = True
                    break
            if responded:
                continue
            # Check for a subsequent issue comment response by pashafateev
            for response in issue_comments:
                print(f"response.user.login: {response.user.login}")
                print(f"comment.user.login: {comment.user.login}")
                print(response.body)
                if (
                    response.created_at > comment.created_at
                    and response.user.login == "pashafateev"
                ):
                    responded_by_tag = "@" + comment.user.login in response.body
                    responded_by_quote = False
                    for line in response.body.splitlines():
                        print(line)
                        print(f"comment.body[:30]: {comment.body[:30]}")
                        if line.strip().startswith(">") and comment.body[:30] in line:
                            responded_by_quote = True
                            break
                    if responded_by_tag or responded_by_quote:
                        responded = True
                        break
            print(f"responded: {responded}")
            print(f"comment.id: {comment.id}")
            print(f"comment_ids_set: {comment_ids_set}")
            if not responded and comment.id not in comment_ids_set:
                unresponded.append(
                    (comment.id, comment.user.login, comment.body, comment.html_url)
                )
                comment_ids_set.add(comment.id)


def process_inline_comments(inline_comments, now, comment_ids_set, unresponded):
    # Process inline review comments (on code)
    for comment in inline_comments:
        if comment.user.login == "pashafateev":
            continue
        if "pashafateev" in comment.body:
            if now - comment.created_at < datetime.timedelta(hours=24):
                continue
            responded = False
            # Check if an emoji reaction from pashafateev exists
            for reaction in comment.get_reactions():
                if reaction.user.login == "pashafateev":
                    responded = True
                    break
            if responded:
                continue
            # Check for a subsequent inline comment from pashafateev
            for response in inline_comments:
                if (
                    response.created_at > comment.created_at
                    and response.user.login == "pashafateev"
                ):
                    responded = True
                    break
            if not responded and comment.id not in comment_ids_set:
                unresponded.append(
                    (comment.id, comment.user.login, comment.body, comment.html_url)
                )
                comment_ids_set.add(comment.id)


@autokitteh.activity
def append_row_to_sheet(id: str, sheet_name: str, values: list):
    """Appends a row to the specified Google Sheet.

    Args:
        spreadsheet_id (str): The Google Spreadsheet ID.
        sheet_name (str): The name of the sheet (tab).
        values (list): List of tuples containing (pr_number, author, body, url).

    Returns:
        dict: API response.
    """
    print("values: ", values)
    range_name = f"{sheet_name}!A:D"  # Use columns A-D for the 4 values
    # Transform list of tuples into list of lists for the API
    formatted_values = [
        [str(comment_id), author, body, url] for comment_id, author, body, url in values
    ]
    body = {"values": formatted_values}

    # Append the rows
    sheets.spreadsheets().values().append(
        spreadsheetId=id,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()


@autokitteh.activity
def get_sheets_data(id: str, sheet_name: str):
    """Get data from the specified Google Sheet.

    Args:
        spreadsheet_id (str): The Google Spreadsheet ID.
        sheet_name (str): The name of the sheet (tab).

    Returns:
        list: List of tuples containing (pr_number, author, body, url).
    """
    range_name = f"{sheet_name}!A:D"
    return (
        sheets.spreadsheets().values().get(spreadsheetId=id, range=range_name).execute()
    )
