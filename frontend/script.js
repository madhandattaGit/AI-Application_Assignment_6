const inputText = document.getElementById("inputText");
const output = document.getElementById("output");
const summarizeButton = document.getElementById("summarizeButton");
const charCount = document.getElementById("charCount");
const wordCount = document.getElementById("wordCount");

// ✅ Update character and word count
function updateCounts() {
    const text = inputText.value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;

    charCount.innerText = `${text.length} chars`;
    wordCount.innerText = `${words} words`;
}

// ✅ Call backend API for summarization
function summarize() {
    const text = inputText.value.trim();

    // Handle empty input (frontend check)
    if (!text) {
        output.classList.add("empty");
        output.innerText = "Please enter some text before summarizing.";
        output.style.color = "red";
        return;
    }

    // Call FastAPI backend
    fetch("http://127.0.0.1:8001/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => {
        output.classList.remove("empty");

        // ✅ Show backend error
        if (data.error) {
            output.innerText = "⚠️ " + data.error;
            output.style.color = "red";
            output.style.backgroundColor = "#ffe6e6";
        } 
        // ✅ Show successful summary
        else {
            output.innerText = data.summary;
            output.style.color = "black";
            output.style.backgroundColor = "#e6ffe6";
        }
    })
    .catch(err => {
        output.innerText = "Error connecting to server.";
        output.style.color = "red";
        console.error(err);
    });
}

// Event listeners
inputText.addEventListener("input", updateCounts);
summarizeButton.addEventListener("click", summarize);

// Initialize counts on load
updateCounts();