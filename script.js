const API_URL = "http://127.0.0.1:5000";

function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || "Upload completed");
        loadFiles();
    })
    .catch(() => alert("Upload failed. Server error."));
}

function loadFiles() {
    fetch(`${API_URL}/files`)
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
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadFiles();
    })
    .catch(() => alert("Delete failed. Server error."));
}

loadFiles();
