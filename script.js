const API = "http://127.0.0.1:5000";

function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch(`${API}/upload`, {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            loadFiles();
        });
}

function loadFiles() {
    fetch(`${API}/files`)
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("filesTable");
            table.innerHTML = `
                <tr>
                    <th>Filename</th>
                    <th>Action</th>
                </tr>
            `;

            data.files.forEach(filename => {
                table.innerHTML += `
                    <tr>
                        <td>${filename}</td>
                        <td><button onclick="deleteFile('${filename}')">Delete</button></td>
                    </tr>
                `;
            });
        });
}

function deleteFile(filename) {
    fetch(`${API}/delete/${filename}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            loadFiles();
        });
}

loadFiles();
