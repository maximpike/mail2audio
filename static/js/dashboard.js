class EmailUploader {
    constructor() {
        this.uploadZone = document.getElementById('uploadZone');
        this.fileInput = document.getElementById('fileInput');
        this.emailListContainer = document.getElementById('emailListContainer');

        this.isUploading = false;

        this.attachEventListeners();
        this.refreshEmailList();
    }

    /*
    * Attach all event listeners for file upload interactions
    * */
    attachEventListeners() {
        this.uploadZone.addEventListener('click', () => {
            this.fileInput.click();
        })

        this.fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                this.handleFileSelect(file);
            }
            event.target.value = '';
        })

        // TODO: DRAG & DROP EVENTS - Prevent default browser behavior (opening the file)

        // Handle the dropped file
        this.uploadZone.addEventListener('drop', (event) => {
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        })
    }

    /*
    * Validate and handle selected file
    * @param {File} file - The file selected by the user
    * */
    handleFileSelect(file) {

        // check file exists
        if (!file) {
            this.showToast('No file selected', 'error');
            return;
        }

        // check file extension
        const fileName = file.name.toLowerCase();
        if (!fileName.endsWith('.eml')) {
            this.showToast('Please select a .eml file', 'error');
            return;
        }

        // check file size
        const maxSizeInBytes = 10 * 1024 * 1024
        if (file.size > maxSizeInBytes) {
            this.showToast('File is too large. Maximum size is 10MB', 'error');
            return;
        }

        console.log('File validated:', fileName, 'Size:', file.size, 'bytes');
        this.uploadFile(file);
    }

    /*
    * Upload the file to the backend API
    * @param {File} file - The validated .eml file
    * */
    async uploadFile(file) {
        this.isUploading = true;

        const uploadStatus = document.getElementById('uploadStatus');
        uploadStatus.innerHTML = `
        <div style="margin-top: 16px; padding: 12px; background: #edf2f7; border-radius: 6px; color: #4a5568;">
                📤 Uploading ${file.name}...
        </div>
        `;

        try {
            const formData = new FormData();
            formData.append('file', file);

            console.log('Sending POST request to /api/emails/upload');

            const response = await fetch('/api/emails/upload', {
                method: 'POST',
                body: formData
            })
            const data = await response.json();

            if (response.ok) {
                console.log('Upload successful:', data);
                this.showToast('Email uploaded successfully!', 'success');
                uploadStatus.innerHTML = ''
                await this.refreshEmailList();
            } else {
                console.error('Upload failed:', data);
                const errorMessage = data.detail || 'Upload failed';
                this.showToast(errorMessage, 'error');
                uploadStatus.innerHTML = '';
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showToast('Network error. Please try again.', 'error');
            uploadStatus.innerHTML = '';
        } finally {
            this.isUploading = false
        }

    }

    /*
    * Display a toast notification
    * @param {string} message - The message to display
    * @param {string} type - 'success' or 'error'
    * */
    showToast(message, type) {
        const config = {
            text: message,
            duration: 3000,
            close: true,
            gravity: 'top',
            position: 'right',
            stopOnFocus: true,
        };

        if (type === 'success') {
            config.style = {
                background: 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)',
            };
        } else if (type === 'error') {
            config.style = {
                background: 'linear-gradient(135deg, #f56565 0%, #e53e3e 100%)',
            }
        }
        Toastify(config).showToast();
    }

    /*
    * Fetch and display the updated email list
    * */
    async refreshEmailList() {
        try {
            this.emailListContainer.innerHTML = '<div class="spinner"></div>';

            console.log('Fetching email list from /api/emails');

            const response = await fetch('/api/emails');

            if (!response.ok) {
                throw new Error('Failed to fecth emails');
            }

            const emails = response.json();

            if (emails.length === 0) {
                // Empty state
                this.emailListContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">📭</div>
                        <div class="empty-text">No emails yet</div>
                    </div>
                `;
            } else {
                // Render email items
                this.emailListContainer.innerHTML = emails.map(emails => `
                    <div class="email-item" onclick="window.location.href='/email/${email.id}'">
                        <div class="audio-status ${email.has_audio ? 'has-audio' : 'no-audio'}">
                            <span class="audio-status-icon">${email.has_audio ? '🔊' : '📧'}</span>
                        </div>
                        <div class="email-info">
                            <div class="email-subject">${this.escapeHtml(email.subject)}</div>
                            <div class="email-meta">
                                From: ${this.escapeHtml(email.sender)} • 
                                ${this.formatDate(email.received_at)}
                            </div>
                        </div>
                    </div>
                `).join('')
            }
        } catch (error) {
            console.error('Error fetching emails:', error);
            this.emailListContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">⚠️</div>
                    <div class="empty-text">Failed to load emails</div>
                </div>
            `;
        }
    }

    /*
    * Escape HTML to prevent XSS attacks
    * @param {string} text - Text to escape
    * @param {string} Escaped text
    * */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /*
    * Format ISO date string to readable format
    * @param {string} dateString - ISO date string
    * @param {string} Formatted date
    * */
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInHours = (now - date) / (1000*60*60);

        if (diffInHours < 24) {
            return date.toLocaleTimeString('en-US', {
                hour: 'numeric',
                minute: '2-digit'
            });
        } else if (diffInHours<48) {
            return 'Yesterday';
        } else {
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric'
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new EmailUploader();
})















