import type {Email} from "../types/email.ts";
import {useNavigate} from "react-router-dom";


interface EmailItemProps {
    email: Email
}

function EmailItem({email}: EmailItemProps) {
    const navigate = useNavigate();

    return (
        <div
            className="email-item"
            onClick={() => navigate(`/email/${email.id}`)}
        >
            <div className={`audio-status ${email.has_audio ? 'has-audio' : 'no-audio'}`}>
                <span className="audio-status-icon">
                    {email.has_audio ? '🔊✅ Available' : '📧⏸️ Not Generated'}
                </span>
            </div>
            <div className="email-info">
                <div className={"email-subject"}>{email.subject}</div>
                <div className="email-meta">
                    From: {email.sender} • {formatDate(email.received_at)}
                </div>
            </div>
        </div>
    );
}

// * Format ISO date string to readable format
function formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000*60*60);

    if (diffInHours < 24) {
        return date.toLocaleTimeString('en-Us', {hour: 'numeric', minute: '2-digit'});
    } else if (diffInHours < 48) {
        return 'Yesterday';
    } else {
        return date.toLocaleDateString('en-US', {month:'short', day: 'numeric'});
    }
}

export default EmailItem;