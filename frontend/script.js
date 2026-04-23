const inputText = document.getElementById("inputText");
const output = document.getElementById("output");
const summarizeButton = document.getElementById("summarizeButton");
const charCount = document.getElementById("charCount");
const wordCount = document.getElementById("wordCount");

function updateCounts() {
    const text = inputText.value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;

    charCount.innerText = `${text.length} chars`;
    wordCount.innerText = `${words} words`;
}

function summarize() {
    const text = inputText.value.trim();

    if (!text) {
        output.classList.add("empty");
        output.innerText = "Please enter some text before summarizing.";
        return;
    }

    const words = text.split(/\s+/);
    const summary = words.slice(0, 20).join(" ");

    output.classList.remove("empty");
    output.innerText = summary + (words.length > 20 ? "..." : "");
}

inputText.addEventListener("input", updateCounts);
summarizeButton.addEventListener("click", summarize);

updateCounts();
