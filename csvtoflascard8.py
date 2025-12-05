<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Flashcard Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }

        .content {
            padding: 40px;
        }

        .upload-area {
            border: 3px dashed #cbd5e1;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s ease;
            background: #f8fafc;
        }

        .upload-area:hover {
            border-color: #4f46e5;
            background: #f1f5f9;
        }

        .upload-area.drag-over {
            border-color: #4f46e5;
            background: #e0e7ff;
        }

        .upload-icon {
            font-size: 48px;
            margin-bottom: 20px;
            color: #4f46e5;
        }

        .file-input {
            display: none;
        }

        .browse-btn {
            background: #4f46e5;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 15px;
        }

        .browse-btn:hover {
            background: #4338ca;
        }

        .selected-file {
            margin-top: 20px;
            padding: 15px;
            background: #e0e7ff;
            border-radius: 8px;
            display: none;
        }

        .selected-file.show {
            display: block;
        }

        .file-name {
            font-weight: 600;
            color: #4f46e5;
        }

        .settings {
            background: #f8fafc;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #475569;
        }

        input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #cbd5e1;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        input[type="number"]:focus {
            outline: none;
            border-color: #4f46e5;
        }

        .process-btn {
            width: 100%;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            margin-top: 10px;
        }

        .process-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4);
        }

        .process-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .progress-container {
            margin-top: 30px;
            display: none;
        }

        .progress-container.show {
            display: block;
        }

        .progress-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .progress-bar {
            height: 12px;
            background: #e2e8f0;
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            width: 0%;
            transition: width 0.5s ease;
            border-radius: 6px;
        }

        .progress-text {
            font-size: 0.9rem;
            color: #64748b;
            text-align: center;
        }

        .result-container {
            margin-top: 30px;
            padding: 25px;
            background: #f0fdf4;
            border: 2px solid #86efac;
            border-radius: 12px;
            display: none;
            text-align: center;
        }

        .result-container.show {
            display: block;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .success-icon {
            font-size: 48px;
            color: #22c55e;
            margin-bottom: 15px;
        }

        .download-btn {
            display: inline-block;
            background: #22c55e;
            color: white;
            text-decoration: none;
            padding: 15px 40px;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 15px;
            transition: background 0.3s;
        }

        .download-btn:hover {
            background: #16a34a;
        }

        .instructions {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 20px;
            margin-top: 30px;
            border-radius: 8px;
        }

        .instructions h3 {
            color: #d97706;
            margin-bottom: 10px;
        }

        .instructions ul {
            list-style-position: inside;
            color: #92400e;
        }

        .instructions li {
            margin-bottom: 8px;
        }

        .error-message {
            background: #fee2e2;
            border: 2px solid #ef4444;
            color: #b91c1c;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }

        .error-message.show {
            display: block;
        }

        .info-box {
            background: #dbeafe;
            border: 2px solid #3b82f6;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }

        .info-box h3 {
            color: #1d4ed8;
            margin-bottom: 10px;
        }

        .info-box p {
            color: #1e40af;
        }

        .loading-spinner {
            display: none;
            width: 40px;
            height: 40px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid #4f46e5;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .mode-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .mode-btn {
            flex: 1;
            padding: 12px;
            border: 2px solid #cbd5e1;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }

        .mode-btn.active {
            background: #4f46e5;
            color: white;
            border-color: #4f46e5;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .upload-area {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 PDF Flashcard Generator</h1>
            <p>Convert your CSV/Excel files into printable flashcards with alternating A/B pattern</p>
        </div>

        <div class="content">
            <!-- Mode Selector -->
            <div class="mode-selector">
                <button class="mode-btn active" onclick="setMode('sync')" id="syncModeBtn">
                    ⚡ Quick Process
                </button>
                <button class="mode-btn" onclick="setMode('async')" id="asyncModeBtn">
                    🔄 Background Process
                </button>
            </div>

            <!-- File Upload Area -->
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <h3>Drag & Drop Your File Here</h3>
                <p>or</p>
                <button class="browse-btn" onclick="document.getElementById('fileInput').click()">
                    Browse Files
                </button>
                <input type="file" id="fileInput" class="file-input" accept=".csv,.xlsx,.xls">
                
                <div class="selected-file" id="selectedFile">
                    Selected: <span class="file-name" id="fileName"></span>
                    <span style="color: #22c55e; margin-left: 10px;">✓</span>
                </div>
            </div>

            <!-- Settings -->
            <div class="settings">
                <div class="form-group">
                    <label for="fontsize">📝 Font Size</label>
                    <input type="number" id="fontsize" value="10" min="5" max="30" step="0.5">
                    <small style="color: #64748b;">Recommended: 10-14 for A6 paper</small>
                </div>
            </div>

            <!-- Process Button -->
            <button class="process-btn" id="processBtn" onclick="processFile()">
                🚀 Generate PDF Flashcards
            </button>

            <!-- Loading Spinner -->
            <div class="loading-spinner" id="loadingSpinner"></div>

            <!-- Progress Container -->
            <div class="progress-container" id="progressContainer">
                <div class="progress-header">
                    <span>Processing...</span>
                    <span id="progressPercent">0%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">
                    Starting processing...
                </div>
            </div>

            <!-- Result Container -->
            <div class="result-container" id="resultContainer">
                <div class="success-icon">✅</div>
                <h3>PDF Generated Successfully!</h3>
                <p>Your flashcards are ready to download.</p>
                <a class="download-btn" id="downloadLink" download>
                    📥 Download PDF
                </a>
                <p style="margin-top: 15px; color: #64748b; font-size: 0.9rem;">
                    File will be automatically downloaded...
                </p>
            </div>

            <!-- Error Message -->
            <div class="error-message" id="errorMessage">
                <strong>Error:</strong> <span id="errorText"></span>
            </div>

            <!-- Info Box -->
            <div class="info-box">
                <h3>📋 Expected File Format</h3>
                <p>Your CSV/Excel file should have:</p>
                <ul style="list-style: none; padding-left: 0;">
                    <li>• Column A: Front of flashcards (odd pages)</li>
                    <li>• Column B: Back of flashcards (even pages)</li>
                    <li>• Optional header row with "Column A", "Front", etc.</li>
                </ul>
            </div>

            <!-- Instructions -->
            <div class="instructions">
                <h3>💡 How It Works</h3>
                <ul>
                    <li>Upload CSV or Excel file with two columns</li>
                    <li>First column = Front side (Column A)</li>
                    <li>Second column = Back side (Column B)</li>
                    <li>PDF will be generated with A6 pages (2 columns × 5 rows)</li>
                    <li>Odd pages show Column A, Even pages show Column B</li>
                    <li>Perfect for printing and cutting into flashcards</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let selectedFile = null;
        let currentMode = 'sync';
        let taskId = null;
        let pollInterval = null;

        // DOM Elements
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const selectedFileDiv = document.getElementById('selectedFile');
        const fileNameSpan = document.getElementById('fileName');
        const processBtn = document.getElementById('processBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const progressPercent = document.getElementById('progressPercent');
        const progressText = document.getElementById('progressText');
        const resultContainer = document.getElementById('resultContainer');
        const downloadLink = document.getElementById('downloadLink');
        const errorMessage = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const syncModeBtn = document.getElementById('syncModeBtn');
        const asyncModeBtn = document.getElementById('asyncModeBtn');

        // Drag and drop handlers
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            
            if (e.dataTransfer.files.length > 0) {
                handleFileSelect(e.dataTransfer.files[0]);
            }
        });

        // File input change handler
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });

        // Handle file selection
        function handleFileSelect(file) {
            // Validate file type
            const validTypes = ['.csv', '.xlsx', '.xls'];
            const fileExt = '.' + file.name.split('.').pop().toLowerCase();
            
            if (!validTypes.includes(fileExt)) {
                showError(`Invalid file type. Please upload: ${validTypes.join(', ')}`);
                return;
            }
            
            // Validate file size (max 10MB)
            if (file.size > 10 * 1024 * 1024) {
                showError('File too large. Maximum size is 10MB.');
                return;
            }
            
            selectedFile = file;
            fileNameSpan.textContent = file.name;
            selectedFileDiv.classList.add('show');
            errorMessage.classList.remove('show');
            
            console.log('File selected:', file.name, 'Size:', file.size);
        }

        // Set processing mode
        function setMode(mode) {
            currentMode = mode;
            
            if (mode === 'sync') {
                syncModeBtn.classList.add('active');
                asyncModeBtn.classList.remove('active');
            } else {
                asyncModeBtn.classList.remove('active');
                asyncModeBtn.classList.add('active');
                syncModeBtn.classList.remove('active');
            }
        }

        // Process file
        async function processFile() {
            if (!selectedFile) {
                showError('Please select a file first.');
                return;
            }
            
            // Reset UI
            errorMessage.classList.remove('show');
            resultContainer.classList.remove('show');
            
            const fontsize = document.getElementById('fontsize').value || 10;
            
            if (currentMode === 'sync') {
                await processSync(fontsize);
            } else {
                await processAsync(fontsize);
            }
        }

        // Synchronous processing
        async function processSync(fontsize) {
            try {
                showLoading(true);
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                formData.append('fontsize', fontsize);
                
                const response = await fetch('/api/process', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    const error = await response.text();
                    throw new Error(error);
                }
                
                // Get the PDF blob
                const blob = await response.blob();
                
                // Create download link
                const url = window.URL.createObjectURL(blob);
                downloadLink.href = url;
                downloadLink.download = `flashcards_${selectedFile.name.split('.')[0]}.pdf`;
                
                // Show result
                showLoading(false);
                resultContainer.classList.add('show');
                
                // Auto-click download link
                setTimeout(() => {
                    downloadLink.click();
                }, 500);
                
            } catch (error) {
                showLoading(false);
                showError(error.message);
            }
        }

        // Asynchronous processing
        async function processAsync(fontsize) {
            try {
                showLoading(true);
                progressContainer.classList.add('show');
                updateProgress(0, 'Uploading file...');
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                formData.append('fontsize', fontsize);
                
                const response = await fetch('/api/process-async', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Upload failed');
                }
                
                taskId = data.task_id;
                showLoading(false);
                
                // Start polling for progress
                startPollingProgress();
                
            } catch (error) {
                showLoading(false);
                showError(error.message);
            }
        }

        // Poll for progress updates
        function startPollingProgress() {
            if (pollInterval) {
                clearInterval(pollInterval);
            }
            
            pollInterval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/progress/${taskId}`);
                    const data = await response.json();
                    
                    if (data.percent !== undefined) {
                        updateProgress(data.percent, data.message);
                    }
                    
                    if (data.status === 'complete') {
                        clearInterval(pollInterval);
                        
                        // Show success
                        setTimeout(() => {
                            progressContainer.classList.remove('show');
                            resultContainer.classList.add('show');
                            downloadLink.href = `/api/download/${taskId}`;
                            downloadLink.download = `flashcards_${taskId}.pdf`;
                            
                            // Auto-download
                            setTimeout(() => {
                                downloadLink.click();
                            }, 1000);
                        }, 1000);
                    }
                    
                    if (data.status === 'error') {
                        clearInterval(pollInterval);
                        showError(data.message);
                    }
                    
                } catch (error) {
                    console.error('Polling error:', error);
                }
            }, 1000);
        }

        // Update progress display
        function updateProgress(percent, message) {
            progressFill.style.width = `${percent}%`;
            progressPercent.textContent = `${Math.round(percent)}%`;
            progressText.textContent = message;
        }

        // Show loading spinner
        function showLoading(show) {
            loadingSpinner.style.display = show ? 'block' : 'none';
            processBtn.disabled = show;
            processBtn.textContent = show ? 'Processing...' : '🚀 Generate PDF Flashcards';
        }

        // Show error message
        function showError(message) {
            errorText.textContent = message;
            errorMessage.classList.add('show');
            
            // Scroll to error
            errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            console.log('PDF Flashcard Generator loaded');
            
            // Set default mode
            setMode('sync');
        });
    </script>
</body>
</html>
