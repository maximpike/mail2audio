import type {Email} from "../types/email.ts";
import type {UploadResponse} from "../types/uploadResponse.ts";

const API_BASE = "/api";

export async function fetchEmails(): Promise<Email[]> {
    const response = await fetch(`${API_BASE}/emails`);
    if (!response.ok) throw new Error("Failed to fetch emails");
    return response.json()
}

export async function fetchEmailById(id: string): Promise<Email> {
    const response = await fetch(`${API_BASE}/emails/${id}`);
    if (!response.ok) throw new Error("Email not found");
    return response.json();
}

export async function uploadEmail(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append("file", file)

    console.log('Sending POST request to /api/emails/upload')

    const response = await fetch(`${API_BASE}/emails/upload`, {
        method: "Post",
        body: formData
    })

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Upload Failed')
    }
    return response.json()
}