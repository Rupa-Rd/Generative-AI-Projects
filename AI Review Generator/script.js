
const apiKey = "";

const feedbackInput = document.getElementById('feedbackInput');
const generateButton = document.getElementById('generateButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const reviewOutput = document.getElementById('reviewOutput');
const reviewText = document.getElementById('reviewText');
const copyButton = document.getElementById('copyButton');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// Ensure all elements are loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', () => {
    if (generateButton) {
        generateButton.addEventListener('click', generateReview);
    } else {
        console.error("Generate button not found!");
    }
    if (copyButton) {
        copyButton.addEventListener('click', copyReviewToClipboard);
    } else {
        console.error("Copy button not found!");
    }
});


async function generateReview() {
    const feedbackDetails = feedbackInput.value.trim();

    if (!feedbackDetails) {
        showError('Please enter some feedback details.');
        return;
    }

    // Clear previous outputs
    reviewOutput.style.display = 'none';
    errorMessage.style.display = 'none';
    loadingIndicator.style.display = 'block';
    generateButton.disabled = true;

    try {
        const prompt = createGeminiPrompt(feedbackDetails);
        const generatedReview = await callGeminiAPI(prompt);

        reviewText.textContent = generatedReview;
        reviewOutput.style.display = 'block';

    } catch (error) {
        console.error('Error generating review:', error);
        showError('Failed to generate review. Please try again. ' + error.message);
    } finally {
        loadingIndicator.style.display = 'none';
        generateButton.disabled = false;
    }
}


function copyReviewToClipboard() {
    const textToCopy = reviewText.textContent;
    if (textToCopy) {
        // Use document.execCommand('copy') for clipboard operations in iframes
        const textArea = document.createElement("textarea");
        textArea.value = textToCopy;
        textArea.style.position = "fixed"; // Prevent scrolling to bottom of page in some browsers
        textArea.style.left = "-9999px";
        textArea.style.top = "-9999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            copyButton.textContent = 'Copied!';
            setTimeout(() => {
                copyButton.textContent = 'Copy Review';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy text. Please copy manually.');
        } finally {
            document.body.removeChild(textArea);
        }
    }
}

function createGeminiPrompt(feedbackDetails) {
    return `Convert the following mobile phone feedback details into a concise, proper English review. Summarize the key points into a coherent sentence or two, focusing on the overall impression. Do not add any introductory or concluding phrases like "Here's the review:" or "In summary:". Just provide the review text.

Feedback details:
${feedbackDetails}

Review:`;
}

async function callGeminiAPI(prompt) {
    let chatHistory = [];
    chatHistory.push({ role: "user", parts: [{ text: prompt }] });

    const payload = { contents: chatHistory };
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`API error: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`);
    }

    const result = await response.json();

    if (result.candidates && result.candidates.length > 0 &&
        result.candidates[0].content && result.candidates[0].content.parts &&
        result.candidates[0].content.parts.length > 0) {
        return result.candidates[0].content.parts[0].text;
    } else {
        throw new Error('Unexpected API response structure or no content generated.');
    }
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    reviewOutput.style.display = 'none';
}
