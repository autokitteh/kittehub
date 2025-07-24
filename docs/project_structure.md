# Contributing to KitteHub

Welcome to KitteHub! This guide will help you contribute new AutoKitteh projects to our repository.

## Project Structure

Each project in KitteHub follows a consistent structure to ensure maintainability and ease of use. Here's what every project should include:

### Required Files

1. **`autokitteh.yaml`** - The project manifest file
2. **`README.md`** - Project documentation following our template
3. **`program.py`** (or main program file) - The main workflow code

### Optional Files

- **`requirements.txt`** - Python dependencies (if using external packages)
- **Additional Python modules** - Helper files, utilities, etc.
- **JSON/Text files** - Configuration, message templates, etc.
- **`images/`** directory - Screenshots or diagrams for documentation

## Directory Structure Examples

### Simple Project

```
my_project/
├── autokitteh.yaml
├── README.md
└── program.py
```

### Complex Project

```
my_project/
├── autokitteh.yaml
├── README.md
├── program.py
├── requirements.txt
├── helpers.py
├── config.json
└── images/
    └── example.png
```

## AutoKitteh Manifest File (`autokitteh.yaml`)

The `autokitteh.yaml` file is the core configuration for your project. Here are common patterns:

### Basic Structure

```yaml
version: v1

project:
  name: your_project_name

  # Optional: Project variables
  vars:
    - name: VARIABLE_NAME
      value: default_value

  # Integration connections
  connections:
    - name: connection_name
      integration: integration_type

  # Triggers for your workflow
  triggers:
    - name: trigger_name
      type: webhook
      call: program.py:function_name
```

### Common Integration Examples

**Slack Integration:**

```yaml
connections:
  - name: slack_conn
    integration: slack

triggers:
  - name: slack_trigger
    connection: slack_conn
    event_type: slash_command
    call: program.py:handle_slash_command
```

**GitHub Integration:**

```yaml
connections:
  - name: github_conn
    integration: github

triggers:
  - name: github_webhook
    connection: github_conn
    event_type: pull_request
    call: program.py:handle_pr
```

**Scheduled Triggers:**

```yaml
triggers:
  - name: daily_check
    schedule: "@daily"
    call: program.py:daily_task
```

## README Documentation

Your README.md must follow our template structure. Use the template at `docs/readme_template.md` and replace all `{PLACEHOLDER}` values.

### Key Requirements

1. **Front matter** with metadata:

   ```yaml
   ---
   title: Your Project Name
   description: One-line description of what it does
   integrations: ["integration1", "integration2"]
   categories: ["Category"]
   tags: ["tag1", "tag2"] # optional
   ---
   ```

> [!NOTE]
> The `integrations` and `categories` values must be from the allowed lists defined in [tests/metadata_definitions.py](../tests/metadata_definitions.py).

2. **Readme structure**:

- Readme file should match the template in [readme_template.md](readme_template.md).

3. **Integration documentation** - Link to relevant AutoKitteh integration docs

## Project Categories

Organize your project in the appropriate directory:

- **`ai_agents/`** - AI-powered automation workflows
- **`devops/`** - Development and operations tools
- **`reliability/`** - Monitoring and incident management
- **`samples/`** - Simple integration examples
- **`walkthroughs/`** - Tutorial projects
- **Root level** - General automation workflows

## Code Quality Guidelines

### Python Code Standards

- Use clear, descriptive function and variable names
- Add docstrings for complex functions
- Handle errors gracefully with try/catch blocks

### AutoKitteh Best Practices

- Always check connection initialization
- Use appropriate logging for debugging
- Handle webhook payloads safely
- Validate input data before processing

### Example Function Structure

```python
import autokitteh

def handle_webhook(event):
    """Handle incoming webhook from external service."""
    try:
        # Validate input
        if not event.data:
            return "No data received"

        # Process the event
        result = process_data(event.data)

        # Return response
        return {"status": "success", "result": result}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
```

## Testing Your Project

Before submitting:

1. **Test locally** - Ensure your code runs without errors
2. **Validate YAML** - Check your `autokitteh.yaml` syntax
3. **Test integrations** - Verify all connections work as expected
4. **Review documentation** - Ensure README is complete and accurate

## Submission Process

1. **Create your project directory** in the appropriate category
2. **Add all required files** (manifest, README, program files)
3. **Follow naming conventions** - Use lowercase with underscores
4. **Test thoroughly** - Ensure everything works as documented
5. **Add projec to readme table** - Run [update_projects_table.py](../update_projects_table.py), doing so will add your project to the readme table
6. **Submit a pull request** with a clear description

## Common Patterns

### Environment Variables

try to use the default connection name:

```yaml
connections:
  - name: <INTERGRATION>_conn
    integration: <INTEGRATION>
```

## Getting Help

- **Documentation**: Check [AutoKitteh docs](https://docs.autokitteh.com)
- **Examples**: Browse existing projects in this repository
- **Issues**: Create an issue for questions or problems

## Review Criteria

Your contribution will be reviewed for:

- ✅ Complete project structure
- ✅ Working `autokitteh.yaml` manifest
- ✅ README following template structure
- ✅ Clean, readable code
- ✅ Appropriate error handling
- ✅ Clear documentation

Thank you for contributing to KitteHub! 🐱
