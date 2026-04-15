let currentMode = 'compress';
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const fileNameDisplay = document.getElementById('file-name');
const processBtn = document.getElementById('process-btn');
const statusContainer = document.getElementById('status-container');
const loader = document.getElementById('loader');
const resultContent = document.getElementById('result-content');
const errorContent = document.getElementById('error-content');
const statsOutput = document.getElementById('stats-output');
const downloadLink = document.getElementById('download-link');
const successMsg = document.getElementById('success-msg');
const errorMsg = document.getElementById('error-msg');

function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(`tab-${mode}`).classList.add('active');

    // Update button text
    processBtn.innerText = mode === 'compress' ? 'Start Compression' : 'Start Decompression';
    resetUI();
}

function resetUI() {
    statusContainer.style.display = 'none';
    loader.style.display = 'none';
    resultContent.style.display = 'none';
    errorContent.style.display = 'none';
}

// File Selection
fileInput.addEventListener('change', handleFileSelect);

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect();
    }
});

function handleFileSelect() {
    if (fileInput.files.length > 0) {
        fileNameDisplay.innerText = fileInput.files[0].name;
        processBtn.disabled = false;
        resetUI();
    }
}

async function processFile() {
    if (!fileInput.files[0]) return;

    // UI Updates
    processBtn.disabled = true;
    statusContainer.style.display = 'block';
    loader.style.display = 'block';
    resultContent.style.display = 'none';
    errorContent.style.display = 'none';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('mode', currentMode);

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        loader.style.display = 'none';

        if (response.ok) {
            resultContent.style.display = 'block';
            successMsg.innerText = currentMode === 'compress' ? 'Compression Successful!' : 'Decompression Successful!';

            const warningEl = document.getElementById('warning-msg');
            if (data.warning) {
                warningEl.innerText = data.warning;
                warningEl.style.display = 'block';
            } else {
                warningEl.style.display = 'none';
            }

            downloadLink.href = data.download_url;
            // Clean up the console output for display
            statsOutput.innerText = data.console_output || 'Process complete.';
        } else {
            errorContent.style.display = 'block';
            errorMsg.innerText = data.error || 'Unknown error occurred.';
        }

    } catch (err) {
        loader.style.display = 'none';
        errorContent.style.display = 'block';
        errorMsg.innerText = 'Network Error: ' + err.message;
    } finally {
        processBtn.disabled = false;
    }
}

// Gen-Z Parallax Effect for Orbs
document.addEventListener('mousemove', (e) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    const orbs = document.querySelectorAll('.orb');
    
    orbs.forEach((orb, index) => {
        const speed = (index + 1) * 20; // Different speeds
        const xOffset = (0.5 - x) * speed;
        const yOffset = (0.5 - y) * speed;
        
        orb.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
});
