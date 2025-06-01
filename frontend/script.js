async function generateToken() {
    const tokenInput = document.getElementById("token");
    const response = await fetch("http://localhost:7000/auth/tokens", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${tokenInput.value}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ isAdmin: false })
    });
    const data = await response.json();
    if (response.ok) {
        tokenInput.value = data.token;
        alert("Token generated!");
    } else {
        alert("Error: " + data.detail);
    }
}

async function moderateImage() {
    const token = document.getElementById("token").value;
    const fileInput = document.getElementById("image").files[0];
    const resultDiv = document.getElementById("result");

    if (!fileInput || !token) {
        resultDiv.innerHTML = "Please provide a token and image.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput);

    const response = await fetch("http://localhost:7000/moderate", {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData
    });
    const data = await response.json();
    if (response.ok) {
        resultDiv.innerHTML = `
            <p>Safe: ${data.is_safe}</p>
            <ul>${data.categories.map(c => `<li>${c.category}: ${c.confidence}</li>`).join("")}</ul>
        `;
    } else {
        resultDiv.innerHTML = "Error: " + data.detail;
    }
}