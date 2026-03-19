export interface Email {
    id: number;
    subject: string;
    sender: string;
    recipient: string;
    received_at: string;
    has_audio: boolean;
    audio_path?: string;
    body_html?: string;
    body_text?: string;
}

