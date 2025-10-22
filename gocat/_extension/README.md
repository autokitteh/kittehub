# Go Links Chrome Extension

A simple Chrome extension that creates personal go links for quick navigation. Transform `go/anything` into redirects to your configured base URL.

## ✨ Features

- 🔗 **Clickable Links**: `<a href="http://go/docs">Link</a>` → redirects to your site
- ⌨️ **Address Bar**: Type `http://go/docs` → instant redirect
- 🔍 **Omnibox**: Type `go<space>docs` in address bar → quick access
- ⚙️ **User Configurable**: Set your own base URL through options page
- 🚫 **No Default URL**: Forces proper setup before use
- 🎯 **Simple Pattern**: `go/anything` → `https://yoursite.com/anything`

## 🚀 Quick Start

### Installation

1. **Download/Clone** this repository
2. **Open Chrome** and go to `chrome://extensions/`
3. **Enable Developer mode** (toggle in top-right corner)
4. **Click "Load unpacked"** and select the extension folder
5. **Configure your base URL** (options page will open automatically)

### First-Time Setup

1. After installation, the options page opens automatically
2. Enter your base URL (e.g., `https://wiki.company.com/`)
3. Click "Save Settings"
4. You're ready to go! 🎉

## ⚙️ Configuration

### Changing Base URL

1. **Right-click** the extension icon → "Options"
2. **Or** go to `chrome://extensions/` → Find "Go Links" → "Details" → "Extension options"
3. **Enter** your new base URL
4. **Click** "Save Settings"

### URL Requirements

- Must be a valid URL (include `https://`)
- Will automatically add trailing slash if missing
- Examples:
  - ✅ `https://wiki.company.com/`
  - ✅ `https://localhost:3000/`
  - ❌ `wiki.company.com` (missing protocol)
  - ❌ `not-a-url` (invalid format)

## 🚨 Limitations

### What Works

- ✅ `http://go/anything` (with protocol)
- ✅ `go anything` (omnibox with space)
- ✅ Clicked links with `http://go/` format

### What Doesn't Work

- ❌ `go/anything` typed directly in address bar (no protocol)

**Why?** Browsers treat `go/anything` as a search query, not a URL. Use `go anything` (with space) instead for address bar shortcuts.

### Workaround for `go/anything`

To make `go/anything` work in the address bar:

1. Chrome Settings → Search engines → Manage search engines
2. Click "Add" next to "Site search"
3. Fill in:
   - **Search engine**: Go Links
   - **Shortcut**: `go`
   - **URL**: `http://go/%s`

Now `go anything` will work in the address bar!
