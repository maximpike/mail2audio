// Authentication State Handling
// You'll eventually need to handle this. Here's the pattern for when you implement it:

// hooks/useAuth.ts (future implementation)
import {useEffect, useState} from "react";

export function useAuth() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function checkAuth() {
            try {
                const response = await fetch('/api/auth/me');
                setIsAuthenticated(response.ok);
            } catch {
                setIsAuthenticated(false);
            } finally {
                setIsLoading(false);
            }
        }
        checkAuth();
    }, []);

    return { isAuthenticated, isLoading };
}

// // Landing.tsx (future update)
// function Landing() {
//     const { isAuthenticated, isLoading } = useAuth();
//     const navigate = useNavigate();
//
//     if (isLoading) {
//         return <div className="spinner" />;
//     }
//
//     return (
//         <div className="page-container">
//         <div className="landing-container">
//             <AppIcon />
//             <h1>Mail2Audio</h1>
//             <p>Transform your email newsletters into audio</p>
//
//     {/* ... features ... */}
//
//     {isAuthenticated ? (
//         <button onClick={() => navigate('/dashboard')} className="primary-btn">
//         Go to Dashboard
//     </button>
//     ) : (
//         <GoogleButton />
//     )}
//     </div>
//     <Footer />
//     </div>
// );
// }
