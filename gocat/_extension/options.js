// Load saved settings and update UI
document.addEventListener("DOMContentLoaded", async function () {
  const result = await chrome.storage.sync.get(["baseUrl"]);
  const baseUrl = result.baseUrl;

  const baseUrlInput = document.getElementById("baseUrl");
  const setupRequired = document.getElementById("setupRequired");
  const currentConfig = document.getElementById("currentConfig");
  const configStatus = document.getElementById("configStatus");

  if (baseUrl && baseUrl.trim() !== "") {
    baseUrlInput.value = baseUrl;
    setupRequired.style.display = "none";
    currentConfig.className = "current-config";
    configStatus.textContent = `Configured: ${baseUrl}`;
  } else {
    setupRequired.style.display = "block";
    currentConfig.className = "current-config not-configured";
    configStatus.textContent = "Not configured - Go Links will not work";
  }
});

// Save settings
document.getElementById("save").addEventListener("click", async function () {
  const baseUrl = document.getElementById("baseUrl").value.trim();

  // Validation
  if (!baseUrl) {
    showStatus("Please enter a base URL", false);
    return;
  }

  try {
    new URL(baseUrl); // Validate URL format
  } catch (e) {
    showStatus("Please enter a valid URL (including https://)", false);
    return;
  }

  // Ensure URL ends with /
  const finalUrl = baseUrl.endsWith("/") ? baseUrl : baseUrl + "/";

  // Save to storage
  await chrome.storage.sync.set({ baseUrl: finalUrl });

  // Update UI
  const setupRequired = document.getElementById("setupRequired");
  const currentConfig = document.getElementById("currentConfig");
  const configStatus = document.getElementById("configStatus");

  setupRequired.style.display = "none";
  currentConfig.className = "current-config";
  configStatus.textContent = `Configured: ${finalUrl}`;

  showStatus("Settings saved successfully! Go Links is now active.", true);
});

// Handle Enter key in input field
document.getElementById("baseUrl").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    document.getElementById("save").click();
  }
});

function showStatus(message, isSuccess) {
  const status = document.getElementById("status");
  status.textContent = message;
  status.className = `status ${isSuccess ? "success" : "error"}`;
  status.style.display = "block";

  // Hide after 3 seconds
  setTimeout(() => {
    status.style.display = "none";
  }, 3000);
}
