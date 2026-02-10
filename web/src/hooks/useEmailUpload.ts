import {useState, useEffect} from 'react';
import {fetchEmails, uploadEmail} from '../services/emailApi';
import type {Email} from '../types/email';

// Check if this is still valid or if it can take bigger files
const MAX_FILE_SIZE = 10 * 1024 * 1024; ///10MB

export function useEmailUpload() {
    const [emails, setEmails] = useState<Email[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        loadEmails();
    }, []);

    async function loadEmails() {
        setIsLoading(true);
        setError(null);
        try {
            const data = await fetchEmails();
            setEmails(data);
        } catch (err) {
            setError('Failed to load emails');
        } finally {
            setIsLoading(false);
        }
    }

    //  Validate and handle selected file
    function validateFie(file: File): { valid: boolean; error?: string } {
        if (!file) {
            return {valid: false, error: "No file selected"};
        }

        const fileName = file.name.toLocaleLowerCase();
        if (!fileName.endsWith('.eml')) {
            return {valid: false, error: "Please select a .eml file"};
        }

        if (file.size > MAX_FILE_SIZE) {
            return {valid: false, error: "File is too large. Maximum size is 10MB"};
        }

        return { valid: true };
    }

    //
    async function handleUpload(file: File) {
        const validation = validateFie(file);
        if (!validation.valid) {
            return { success: false, error: validation.error };
        }

        setIsUploading(true);
        setError(null);
        try {
            await uploadEmail(file);
            await loadEmails();
            return {success: true};
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Upload failed';
            setError(message);
            return {success: false, error: message};
        } finally {
            setIsUploading(false);
        }
    }

    return {
        emails,
        isLoading,
        isUploading,
        error,
        handleUpload,
        refreshEmails: loadEmails,
    };
}