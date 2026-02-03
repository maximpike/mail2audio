

function EmailDetail() {
    return(
        <div className="page-container">
            <div className="email-detail-container">
                {/*Back Button*/}
                <a href="/dashboard" className="back-button">
                    ← Back to Dashboard
                </a>

                {/*Email Detail Card*/}
                <div className="email-detail-card">
                    {/*Header*/}
                    <div className="email-header">
                        <h1 className="email-subject-large"> {{email.subject}}</h1>

                        <div className="email-metadata">
                            <div className="metadata-item">
                                <div className="metadata-label">From</div>
                                <div className="metadata-value"> {{email.sender}}</div>
                            </div>
                            <div className="metadata-item">
                                <div className="metadata-label">To</div>
                                <div className="metadata-value">{{email.recipient}}</div>
                            </div>
                            <div className="metadata-item">
                                <div className="metadata-label">Date</div>
                                <div className="metadata-value">{{
                                    email.received_date.strftime('%B %d, %Y at %I:%M %p') if
                                    email.received_date else 'Unknown'
                                }}
                                </div>
                            </div>
                            <div className="metadata-item">
                                <div className="metadata-label">Audio Status</div>
                                <div className="metadata-value">
                                    {% if email.has_audio %}
                                    ✅ Available
                                    {% else %}
                                    ⏸️ Not Generated
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/*Audio Player */}
                    {/*{% if email.has_audio %}*/}
                    <div className="audio-player-section">
                        <div className="audio-player-label">🔊 Audio Version</div>
                        <audio controls style="width: 100%;">
                            <source src="{{ email.audio_path }}" type="audio/mpeg"/>
                            Your browser does not support the audio element
                        </audio>
                    </div>
                    {/*{% else %}*/}
                    <div className="audio-player-section">
                        <div className="no-audio-message">
                            <div>⏸️ Audio not yet generated</div>
                            <div style="font-size: 14px; margin-top: 8px; color: #718096;">
                                Audio generation coming soon!
                            </div>
                        </div>
                    </div>
                    {/*{% endif %}*/}

                    {/*Audio Player */}
                    <div className="email-body">
                        {/*{% if email.body_html %}*/}
                        <div>{{email.body_html | safe}}</div>
                        {/*{% elif email.body_text %}*/}
                        <pre style="white-space: pre-wrap; font-family: inherit;">{{email.body_text}}</pre>
                        {/*{% else %}*/}
                        <p style="color: #a0aec0;">No content available</p>
                        {/*{% endif %}*/}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default EmailDetail