// Dashboard.tsx
import "../App.css"
import "../styles/Dashboard.css"
import {useRef} from "react";
import {useEmailUpload} from "../hooks/useEmailUpload.ts";
import EmailItem from "../components/EmailItem.tsx";
import {toast} from 'react-toastify';

function Dashboard() {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const {emails, isLoading, isUploading, error, handleUpload} = useEmailUpload();

    const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const result = await handleUpload(file)
            if (result.success) {
                toast.success("Email uploaded successfully!");
            } else {
                toast.error(result.error || "Upload failed");
            }
        }
        e.target.value = '';  // Reset input
    }

    const onDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) {
            await handleUpload(file);
        }
    };

    return (
        <div className="page-container">
            <div className="dashboard-container">
                {/*//Header*/}
                <div className="dashboard-header">
                    <h1 className="dashboard-title">📧 Mail2Audio Dashboard</h1>
                </div>

                {/* Email List */}
                <div className="email-list">
                    {isLoading && <div className="spinner"/>}
                    {error && <div className="error">{error}</div>}
                    {!isLoading && emails.length === 0 && (
                        <div className="empty-state">
                            <div className="empty-icon">📭</div>
                            <div className="empty-text">No emails yet</div>
                        </div>
                    )}
                    {emails.map((email) => (
                        <EmailItem key={email.id} email={email}/>
                    ))}
                </div>
                {/* Upload Zone */}
                <div className="upload-section">
                    <div
                        className="upload-zone"
                        onClick={() => fileInputRef.current?.click()}
                        onDrop={onDrop}
                        onDragOver={(e) => e.preventDefault()}
                    >
                        <div className="upload-icon">📤</div>
                        <div className="upload-text">
                            {isUploading ? 'Uploading...' : 'Drop your .eml file here'}
                        </div>
                        <input
                            ref={fileInputRef}
                            type="file"
                            className="file-input"
                            accept=".eml"
                            onChange={onFileChange}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;