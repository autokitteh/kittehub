---
title: Gocat - URL Shortener & Redirector
description: Simple URL shortener using Google Sheets as a data store with webhook-based redirection
integrations: ["googlesheets"]
categories: ["Productivity"]
tags: ["webhook_handling", "sync_responses"]
---

# Gocat - URL Shortener

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=gocat)

Gocat is a simple "go links" URL shortener and redirector that uses Google Sheets as its data store. It maps short keys to full URLs via webhook, providing an easy way to manage and share shortened links.

![demo](https://raw.githubusercontent.com/autokitteh/kittehub/main/gocat/demo.gif)

## What are Go Links?

Go links (also known as "go/" links) are short, memorable internal URLs that redirect to longer, harder-to-remember URLs. They're commonly used within organizations to make it easier to access frequently-used resources.

Instead of remembering something like:
https://docs.google.com/document/d/1a2b3c4d5e6f7g8h9i0j/edit

You can create a go link like:
`go/team-onboarding`

## Features

- **Google Sheets Backend**: Edit URLs directly in a spreadsheet - no admin UI needed
- **Multiple Matches**: If a key has multiple URLs, displays an HTML page with all options
- **Path Appending**: Append additional path segments to the target URL
- **Lightweight**: ~200 lines of Python with no external state or databases
- **Direct Access**: No suffix redirects to the spreadsheet for quick editing

## Why?

The entire URL shortener is ~200 lines of Python. With AutoKitteh, you get:

- **No database needed**: Google Sheets is your data store - edit URLs directly in a familiar spreadsheet interface
- **Instant deployment**: Deploy with `make deploy` and get a webhook URL
- **No infrastructure**: No servers, databases, or state management to worry about
- **Full control**: Customize the logic by editing Python code
- **Easy sharing**: Share the Google Sheet with your team to collaboratively manage URLs

### What [AutoKitteh](https://autokitteh.com) Provides

- Production ready without the complexity
- Webhook endpoints
- Built-in Google Sheets integration (and others)
- Synchronous HTTP responses
- No web server configuration needed

### GoCat vs. Commercial Shorteners

- Dead simple
- No link expiration
- No tracking or analytics collection
- Own your data - it's just a Google Sheet
- Free to run (no per-link or per-click pricing)
- Customize behavior (e.g., add authentication, logging, custom responses)

## How It Works

1. **Create a Google Spreadsheet** with two columns:

   - Column 1: Short keys (e.g., "docs", "api")
   - Column 2: Full URLs (e.g., "https://example.com/documentation")

2. **Deploy to AutoKitteh**: [![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=gocat) get a webhook URL like `https://api.autokitteh.cloud/webhooks/<slug>`

3. **Access shortened URLs**: Visit `https://api.autokitteh.cloud/webhooks/<slug>/docs`
   - Redirects to the URL mapped to "docs" in your spreadsheet

## Making the Browser understand Go links

The following methods are the simplest to make Chrome to understand go links.

## 1. Chrome Search Engine

**What it does:** Treats `go` as a search keyword that redirects

**Setup:**

Chrome Settings → Search engines → Add custom search engine

- Keyword: `go`
- URL: `https://api.autokitteh.cloud/webhooks/<slug>/%s`

## 2. Browser Extension

For a better user experience, you can use the included Chrome extension in the `_extension` directory. This allows you to use short go links directly in your browser:

- Type `go/docs` in your address bar to redirect to your shortened URLs
- Click on links like `<a href="http://go/docs">` in web pages
- Use the omnibox with `go<space>docs` for quick access

**Setup:**

1. Follow the installation instructions in `_extension/README.md`
2. Configure the extension's base URL to your AutoKitteh webhook URL (e.g., `https://api.autokitteh.cloud/webhooks/<slug>`)
3. Now you can use `go/docs` instead of typing the full webhook URL

See `_extension/README.md` for detailed setup and configuration instructions.

## Usage

1. **Create a new Google Spreadsheet** in your Google Drive
2. **Set up two columns**:

   ```
   Column 1 (Short Key) | Column 2 (Full URL)
   ---------------------|--------------------
   docs                 | https://example.com/documentation
   api                  | https://example.com/api
   github               | https://github.com/myorg/myrepo
   ```

3. **Copy the Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```

Once deployed, you'll have a webhook URL like `https://api.autokitteh.cloud/webhooks/<slug>`. Here's how to use it:

- **No path** (`/webhooks/<slug>`): Redirects to your Google Spreadsheet for easy editing
- **With short key** (`/webhooks/<slug>/docs`): Redirects to the URL mapped to "docs"
- **With additional path** (`/webhooks/<slug>/api/v1/users`): Redirects to the URL for "api" with `/v1/users` appended

### Multiple Matches

If your spreadsheet has multiple entries for the same key:

```
docs | https://example.com/docs
docs | https://docs.example.org
```

Accessing `/webhooks/<slug>/docs` returns an HTML page with both links.

## Configuration

Configure the system using project variables in `autokitteh.yaml`:

- `GOOGLE_SPREADSHEET_ID`: ID of the Google Sheet storing URL mappings (required)
- `DIRECTORY_SHEET_NAME`: Name of the sheet to use (optional, defaults to first sheet)

Update these values in `autokitteh.yaml` before deploying, or modify using the AutoKitteh UI after.

```yaml
vars:
  - name: GOOGLE_SPREADSHEET_ID
    value: "YOUR_SPREADSHEET_ID_HERE"
  - name: DIRECTORY_SHEET_NAME
    value: "" # Leave empty to use the first sheet
```

## Connections

- **gsheets** (required): Google Sheets integration for reading URL mappings

## Implementation Details

### Core Files

- **`handlers.py`** (`handlers.py:48`): Main webhook handler that processes requests

  - `on_webhook()`: Extracts suffix, queries store, returns HTTP response
  - `_extract_suffix()`: Parses webhook path to extract the lookup key

- **`store.py`** (`store.py:49`): Google Sheets interface
  - `find(path)`: Searches column 1 for matching keys, returns URLs from column 2
  - `spreadsheet_url()`: Returns the Google Sheets URL for direct access

### How It Uses AutoKitteh

The system uses 2 AutoKitteh features:

```python
from autokitteh import Event, http_outcome
```

1. **Webhook Triggers** (`autokitteh.yaml:22`): Synchronous GET webhook

   ```yaml
   triggers:
     - name: webhook
       type: webhook
       call: handlers.py:on_webhook
       event_type: get
       is_sync: true
   ```

2. **HTTP Responses** (`handlers.py:69`): Return HTTP redirects
   ```python
   http_outcome(302, headers={"Location": target_url})
   ```

The rest is regular Python logic for path parsing and Google Sheets lookups.

## Development

Run checks locally:

```bash
make
```

## Deployment

To deploy to AutoKitteh:

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Update configuration**: Edit `autokitteh.yaml` with your `GOOGLE_SPREADSHEET_ID`
4. **Deploy**: `make deploy`
5. **Initialize connection**: Log in to https://autokitteh.cloud and initialize the Google Sheets connection

After deployment, you'll receive a webhook URL that you can use to access your shortened URLs.
