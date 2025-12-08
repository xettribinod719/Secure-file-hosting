const API_URL = "http://127.0.0.1:5000";

function getToken() {
    return localStorage.getItem("token");
}

function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const uploadBtn = document.getElementById("uploadBtn");
    const loader = document.getElementById("loader");

    if (!getToken()) {
        alert("Login required");
        window.location.href = "/login";
        return;
    }

    if (fileInput.files.length === 0) {
        alert("No file selected");
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
            alert(data.message || "Upload completed");
            loadFiles();
        })
        .catch(() => alert("Upload failed. Server error."))
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
            table.innerHTML = `
                <tr>
                    <th>Filename</th>
                    <th>Action</th>
                </tr>
            `;
            (data.files || []).forEach(filename => {
                table.innerHTML += `
                    <tr>
                        <td>${filename}</td>
                        <td><button onclick="deleteFile('${filename}')">Delete</button></td>
                    </tr>
                `;
            });
        })
        .catch(() => alert("Failed to load files."));
}

function deleteFile(filename) {
    fetch(`${API_URL}/delete/${filename}`, {
        method: "DELETE",
        headers: { "Authorization": getToken() }
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            loadFiles();
        })
        .catch(() => alert("Delete failed. Server error."));
}

loadFiles();
