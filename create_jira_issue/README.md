# Create Atlassian Jira Issues

## Sources

- HTTP GET webhook (URL path `/http/create_jira_issue` + query parameters)
- HTTP POST webhook (same URL path, but with a form or a JSON body)

## HTTP Trigger Examples

HTTP GET request with query parameters in the URL (basic Jira fields):

```
curl "http://localhost:9980/http/create_jira_issue/webhook?key1=val1&key2=val2"
```

HTTP POST request with a URL-encoded form body (basic Jira fields):

```
curl -X POST "http://localhost:9980/http/create_jira_issue/webhook" \
     -d key1=val1 -d key2=val2
```

HTTP POST request with a JSON body (unlimited Jira fields):

```
curl -X POST "http://localhost:9980/http/create_jira_issue/webhook" \
     -H "Content-Type: application/json" -d '{"key1": "val1", "key2": "val2"}'
```

## Basic Parameters Example

```json
{
  "project": "TEST",
  "issuetype": "Task",
  "summary": "Test issue",
  "description": "This is a test issue"
}
```
