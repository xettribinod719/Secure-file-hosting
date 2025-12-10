const API_URL = "http://127.0.0.1:5000";

console.log("Script loaded. API_URL:", API_URL);

function getToken() {
    return localStorage.getItem("token");
}

function saveToken(token) {
    localStorage.setItem("token", token);
    console.log("Token saved to localStorage");
}

function removeToken() {
    localStorage.removeItem("token");
    console.log("Token removed from localStorage");
}

function showMessage(text, type = "success") {
    console.log("Showing message:", text, type);

    // Create message box if it doesn't exist
    let msgBox = document.getElementById("msgBox");
    if (!msgBox) {
        msgBox = document.createElement("div");
        msgBox.id = "msgBox";
        msgBox.style.position = "fixed";
        msgBox.style.top = "20px";
        msgBox.style.right = "20px";
        msgBox.style.padding = "15px 25px";
        msgBox.style.borderRadius = "5px";
        msgBox.style.zIndex = "1000";
        msgBox.style.color = "white";
        msgBox.style.fontWeight = "bold";
        msgBox.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
        msgBox.style.transition = "all 0.3s ease";
        document.body.appendChild(msgBox);
    }

    msgBox.innerText = text;
    msgBox.style.backgroundColor = type === "success" ? "#4CAF50" : "#f44336";
    msgBox.style.display = "block";

    setTimeout(() => {
        msgBox.style.display = "none";
    }, 5000);
}

// API fetch helper
async function apiFetch(url, options = {}, requireAuth = false) {
    console.log("apiFetch called:", url, options);

    const headers = options.headers || {};

    if (requireAuth) {
        const token = getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
            console.log("Added Authorization header");
        } else {
            console.warn("No token found for auth-required request");
        }
    }

    if (!(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    const config = {
        ...options,
        headers
    };

    try {
        console.log("Fetching:", url, config);
        const response = await fetch(url, config);
        console.log("Response status:", response.status, response.statusText);

        let data = {};
        try {
            data = await response.json();
            console.log("Response data:", data);
        } catch (jsonError) {
            console.log("JSON parse error (might be empty response):", jsonError);
        }

        return {
            ok: response.ok,
            status: response.status,
            data: data
        };
    } catch (error) {
        console.error("Network error in apiFetch:", error);
        return {
            ok: false,
            status: 0,
            data: { error: "Network error: " + error.message }
        };
    }
}

// Upload function
async function uploadFile() {
    console.log("uploadFile called");

    const fileInput = document.getElementById("fileInput");
    const uploadBtn = document.getElementById("uploadBtn");
    const loader = document.getElementById("loader");

    if (!getToken()) {
        showMessage("Login required", "error");
        window.location.href = "/login";
        return;
    }

    if (fileInput.files.length === 0) {
        showMessage("No file selected", "error");
        return;
    }

    uploadBtn.disabled = true;
    if (loader) loader.style.display = "inline-block";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Add privacy if exists
    const privacySelect = document.querySelector('select[name="privacy"]');
    if (privacySelect) {
        formData.append("privacy", privacySelect.value);
    }

    const result = await apiFetch(`${API_URL}/api/upload`, {
        method: "POST",
        body: formData
    }, true);

    if (result.ok) {
        showMessage(result.data.message || "Upload successful");
        // Load files if on index page
        if (typeof loadFiles === 'function') {
            loadFiles();
        }
    } else {
        showMessage(result.data.error || "Upload failed", "error");
    }

    uploadBtn.disabled = false;
    if (loader) loader.style.display = "none";
}

// Rest of the functions remain the same...
// [Keep the rest of your script.js code as is]
