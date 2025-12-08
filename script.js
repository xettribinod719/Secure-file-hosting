const API_URL = "http://127.0.0.1:5000";

function getToken() {
    return localStorage.getItem("token");
}

function showMessage(text, type = "success") {
    const msg = document.getElementById("msgBox");
    msg.innerText = text;
    msg.className = type === "success" ? "msg-success" : "msg-error";
}

function uploadFile() {
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
    loader.style.display = "inline-block";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch(`${API_URL}/upload`, {
        method: "POST",
        headers: { "Authorization": getToken() },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        showMessage(data.message || "Upload successful");
        loadFiles();
    })
    .catch(() => showMessage("Upload failed", "error"))
    .finally(() => {
        uploadBtn.disabled = false;
        loader.style.display = "none";
    });
}

function loadFiles() {
    fetch(`${API_URL}/files`, {
        headers: { "Authorization": getToken() }
    })
    .then(res => res.json())
    .then(data => {
        const table = document.getElementById("filesTable");
        const count = document.getElementById("fileCount");

        table.innerHTML = `
            <tr>
                <th>Filename</th>
                <th>Action</th>
            </tr>
        `;

        const files = data.files || [];
        count.innerText = `Total Files: ${files.length}`;

        files.forEach(filename => {
            table.innerHTML += `
                <tr>
                    <td>${filename}</td>
                    <td><button onclick="deleteFile('${filename}')">Delete</button></td>
                </tr>
            `;
        });
    })
    .catch(() => showMessage("Failed to load files", "error"));
}

function deleteFile(filename) {
    fetch(`${API_URL}/delete/${filename}`, {
        method: "DELETE",
        headers: { "Authorization": getToken() }
    })
        .then(res => res.json())
        .then(data => {
            showMessage(data.message);
            loadFiles();
        })
        .catch(() => showMessage("Delete failed", "error"));
}

loadFiles();
setInterval(loadFiles, 5000);
