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

    // Update button text with more friendly terms
    const btnText = document.getElementById('btn-text');
    btnText.innerText = mode === 'compress' ? 'Shrink My File' : 'Restore My File';
    resetUI();
}


function resetUI() {
    statusContainer.style.display = 'none';
    loader.style.display = 'none';
    resultContent.style.display = 'none';
    errorContent.style.display = 'none';
}

// File Selection
dropZone.addEventListener('click', () => {
    fileInput.click();
});

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
            successMsg.innerText = currentMode === 'compress' ? 'Shrink Successful' : 'Restore Successful';

            // Parse Stats from Console Output
            if (data.console_output) {
                const output = data.console_output;
                const originalMatch = output.match(/Original Size:\s+(\d+)/);
                const compressedMatch = output.match(/Compressed Size:\s+(\d+)/);
                const ratioMatch = output.match(/Compression Ratio:\s+([\d.]+)%/);

                if (originalMatch) document.getElementById('stat-original').innerText = formatBytes(originalMatch[1]);
                if (compressedMatch) document.getElementById('stat-compressed').innerText = formatBytes(compressedMatch[1]);
                if (ratioMatch) document.getElementById('stat-savings').innerText = ratioMatch[1] + '%';
            }

            const warningEl = document.getElementById('warning-msg');
            if (data.warning) {
                warningEl.innerText = data.warning;
                warningEl.style.display = 'block';
            } else {
                warningEl.style.display = 'none';
            }

            downloadLink.href = data.download_url;
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
