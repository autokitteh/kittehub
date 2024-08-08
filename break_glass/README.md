# Break Glass Request and Approval Orchestration

This program orchestrates the request and approval process for break glass scenarios, where a developer needs elevated permissions to access sensitive data or perform critical operations beyond their usual access.

## Benefits

1. **Controlled Access**: Ensures sensitive data and operations are only accessible when necessary and with proper approval.
2. **Audit Trail**: Maintains a clear record of who requested and approved access, providing transparency and accountability.
3. **Automated Workflow**: Streamlines the request and approval process through automation, reducing manual overhead and potential for errors.

## How It Works

1. **Request Initiation**:
   - A developer initiates the process using a Slack slash command to request break glass approval.

2. **Information Gathering**:
   - AutoKitteh sends a form to the developer, requesting details about the reason for the elevated access.
   - The developer fills out the form, providing the necessary information and justification.

3. **Verification**:
   - The program integrates with Jira to verify the existence of the ticket and ensure the requester is the ticket's assignee.

4. **Approval Request**:
   - AutoKitteh sends a notification to the Site Reliability Engineering (SRE) team with an approve/deny message, including the details of the request.
   - The SRE team reviews the request and makes a decision.

5. **Notification**:
   - AutoKitteh notifies the developer of the decision via Slack, indicating whether the request was approved or denied.

6. **Permission Management**:
   - If approved, permissions are granted to the developer, with a set expiration time.
   - The system monitors the permissions and automatically removes them once they expire, ensuring minimal risk.

7. **Integration with Services**:
   - The program uses Slack for communication and notifications.
   - It also integrates with AWS for permission management, Redis for storing timestamps, and Google Sheets for tracking purposes.

## Usage

To use this program, ensure you have the necessary environment variables set, such as `APPROVAL_CHANNEL`, `SHEET_ID`, `SHEETS_RANGE`, and other connection details for AWS, Google Sheets, Jira, Redis, and Slack.

The workflow begins when a developer uses the Slack slash command to initiate a break glass request. The program then follows the outlined steps to ensure controlled, auditable access to sensitive resources.
