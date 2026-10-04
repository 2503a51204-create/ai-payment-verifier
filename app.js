const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const copyBtn = document.getElementById("copy");
const historyBtn = document.getElementById("historyBtn");

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) {
        fileName.textContent = "No file selected";
        analyzeBtn.disabled = true;
        return;
    }

    const maxSize = 10 * 1024 * 1024;

    if (file.size > maxSize) {
        fileName.textContent = "File is larger than 10 MB.";
        analyzeBtn.disabled = true;
        return;
    }

    fileName.textContent = `Selected: ${file.name}`;
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "🔍 Analyze Evidence";
});

analyzeBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "⏳ Analyzing...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.error || "Analysis failed.");
        }

        updateResults(result);

        document.querySelector(".results").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        alert(error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "🔍 Analyze Again";
    }
});

function updateResults(result) {
    document.getElementById("score").textContent = result.score;

    if (result.risk_level === "low") {
        document.getElementById("scoreMessage").textContent = "Low risk detected";
    } else if (result.risk_level === "medium") {
        document.getElementById("scoreMessage").textContent = "Review recommended";
    } else {
        document.getElementById("scoreMessage").textContent = "High risk detected";
    }

    document.getElementById("integrity").textContent =
        "✓ " + result.integrity.status;

    document.getElementById("content").textContent =
        "✓ " + result.content.status;

    document.getElementById("metadata").textContent =
        "✓ " + result.metadata.status;

    document.getElementById("ai").textContent =
        "• " + result.ai.label;

    document.getElementById("verdict").textContent =
        result.status;

    document.getElementById("reason").textContent =
        result.ai.reason;

    document.getElementById("hash").textContent =
        result.hash;

    document.getElementById("preview").textContent =
        result.content.preview || "No text could be extracted.";
}

copyBtn.addEventListener("click", async () => {
    const hash = document.getElementById("hash").textContent;

    if (!hash || hash === "Not generated yet") {
        return;
    }

    try {
        await navigator.clipboard.writeText(hash);
        copyBtn.textContent = "Copied!";
        setTimeout(() => {
            copyBtn.textContent = "Copy";
        }, 1200);
    } catch (_error) {
        alert("Could not copy the fingerprint.");
    }
});

historyBtn.addEventListener("click", async () => {
    const panel = document.getElementById("history");

    panel.classList.toggle("hidden");

    if (panel.classList.contains("hidden")) {
        return;
    }

    const box = document.getElementById("historyData");
    box.textContent = "Loading...";

    try {
        const response = await fetch("/history");
        const data = await response.json();

        if (!response.ok) {
            throw new Error("Could not load history.");
        }

        if (!data.items.length) {
            box.textContent = "No verification history yet.";
            return;
        }

        box.innerHTML = data.items.map((item) => `
            <div class="history-item">
                <div>
                    <strong>${escapeHtml(item.file_name)}</strong>
                    <span>${escapeHtml(item.status)}</span>
                </div>
                <div>
                    <b>${item.score}/100</b>
                    <small>${escapeHtml(item.created_at)}</small>
                </div>
            </div>
        `).join("");

    } catch (error) {
        box.textContent = error.message;
    }
});

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
