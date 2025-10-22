// Get the base URL from storage (no default)
async function getBaseUrl() {
  const result = await chrome.storage.sync.get(["baseUrl"]);
  return result.baseUrl; // Will be undefined if not set
}

// Check if extension is configured
async function isConfigured() {
  const baseUrl = await getBaseUrl();
  return baseUrl && baseUrl.trim() !== "";
}

// Show setup notification
function showSetupNotification() {
  chrome.notifications.create({
    type: "basic",
    iconUrl:
      "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjAiIGZpbGw9IiM0Mjg1ZjQiLz4KPHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSI+CjxwYXRoIGQ9Ik0yNCAzNlYyNE0yNCAyNEwyNCAyNE0yNCAyNEwyNCAyNE0yNCAyNEwyNCAyNE0yNCAyNEwyNCAyNCIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+",
    title: "Go Links Setup Required",
    message: "Please configure your base URL in the extension options first.",
  });
}

// Update redirect rules when base URL changes
async function updateRedirectRules() {
  const baseUrl = await getBaseUrl();

  // Remove existing rules
  const existingRules = await chrome.declarativeNetRequest.getDynamicRules();
  const ruleIdsToRemove = existingRules.map((rule) => rule.id);

  await chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: ruleIdsToRemove,
    addRules: [], // Remove all rules initially
  });

  // Only add rule if baseUrl is configured
  if (baseUrl && baseUrl.trim() !== "") {
    const newRules = [
      {
        id: 1,
        priority: 1,
        action: {
          type: "redirect",
          redirect: {
            regexSubstitution: baseUrl + "\\1",
          },
        },
        condition: {
          regexFilter: "^https?://go/(.*)$",
          resourceTypes: ["main_frame", "sub_frame"],
        },
      },
    ];

    await chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: [],
      addRules: newRules,
    });
  }
}

// Handle omnibox input (for "go<space>whatever" in address bar)
chrome.omnibox.onInputEntered.addListener(async function (text) {
  const configured = await isConfigured();

  if (!configured) {
    // Open options page if not configured
    chrome.runtime.openOptionsPage();
    return;
  }

  const baseUrl = await getBaseUrl();
  const redirectUrl = baseUrl + text;
  chrome.tabs.update({ url: redirectUrl });
});

// Handle extension icon clicks to open options if not configured
chrome.action.onClicked.addListener(async function () {
  const configured = await isConfigured();

  if (!configured) {
    chrome.runtime.openOptionsPage();
  } else {
    // Could show a popup or just open options anyway
    chrome.runtime.openOptionsPage();
  }
});

// Initialize rules on startup
chrome.runtime.onStartup.addListener(updateRedirectRules);
chrome.runtime.onInstalled.addListener(async function (details) {
  await updateRedirectRules();

  // Show setup notification on first install
  if (details.reason === "install") {
    const configured = await isConfigured();
    if (!configured) {
      chrome.runtime.openOptionsPage();
    }
  }
});

// Listen for storage changes to update rules
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === "sync" && changes.baseUrl) {
    updateRedirectRules();
  }
});
