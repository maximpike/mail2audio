import {useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import type {Email} from "../types/email.ts";
import {fetchEmailById} from "../services/emailApi.ts";


function EmailDetail() {
    const {id} = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [email, setEmail] = useState<Email | null>(null);
    const [isLoading, setisLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadEmail() {
            if (!id) return;

            setisLoading(true)
            setError(null);
            try {
                const data = await fetchEmailById(id);
                setEmail(data);
            } catch(err) {
                setError(err instanceof Error ? err.message : "Failed to load email");
            } finally {
                setisLoading(false);
            }
        }
        loadEmail();
    }, [id])

    // Loading state
    if (isLoading) {
        return (
            <div className="page-container">
                <div className="email-detail-container">
                    <div className="spinner" />
                </div>
            </div>
        );
    }

    // Error state
    if (error || !email) {
        return (
            <div className="page-container">
                <div className="email-detail-container">
                    <button className="back-button" onClick={() => navigate("/dashboard")}>
                        ← Back to Dashboard
                    </button>
                    <div className="empty-state">
                        <div className="empty-icon">⚠️</div>
                        <div className="empty-text">{error || "Email not found"}</div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container">
            <div className="email-detail-container">
                {/*Back Button*/}
                <button className="back-button" onClick={() => navigate("/dashboard")}>
                    ← Back to Dashboard
                </button>

                {/*Email Detail Card*/}
                <div className="email-detail-card">
                    {/*Header*/}
                    <div className="email-header">
                        <h1 className="email-subject-large">{email.subject}</h1>

                        <div className="email-metadata">
                            <div className="metadata-item">
                                <div className="metadata-label">From</div>
                                <div className="metadata-value">{email.sender}</div>
                            </div>
                            <div className="metadata-item">
                                <div className="metadata-label">To</div>
                                <div className="metadata-value">{email.recipient}</div>
                            </div>
                            <div className="metadata-item">
                                <div className="metadata-label">Date</div>
                                <div className="metadata-value">{formatDate(email.received_at)}</div>
                            </div>
                            <div className="metadata-item">
                                <div className="metadata-label">Audio Status</div>
                                <div className="metadata-value">
                                    {email.has_audio ? "✅ Available" : "⏸️ Not Generated"}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Audio Player */}
                    <div className="audio-player-section">
                        {email.has_audio ? (
                            <>
                                <div className="audio-player-label">🔊 Audio Version</div>
                                <audio controls style={{ width: "100%" }}>
                                    <source src={email.audio_path} type="audio/mpeg" />
                                    Your browser does not support the audio element
                                </audio>
                            </>
                        ) : (
                            <div className="no-audio-message">
                                <div>⏸️ Audio not yet generated</div>
                                <div style={{ fontSize: "14px", marginTop: "8px", color: "#718096" }}>
                                    Audio generation coming soon!
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Email Body */}
                    <div className="email-body">
                        {email.body_html ? (
                            <div dangerouslySetInnerHTML={{ __html: email.body_html }} />
                        ) : email.body_text ? (
                            <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>
                                {email.body_text}
                            </pre>
                        ) : (
                            <p style={{ color: "#a0aec0" }}>No content available</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
    });
}


export default EmailDetail;