import "../styles/Landing.css";
import "../App.css";
import AppIcon from "../components/AppIcon.tsx";
import Footer from "../components/Footer/Footer.tsx";
import GoogleButton from "../components/GoogleButtons/GoogleButton.tsx"


function Landing() {
    return (
        <div className="page-container">
            <div className="landing-container">
                <AppIcon />
                <h1>Mail2Audio</h1>
                <p>Transform you email newsletters into audio</p>

                <div className="features-container">
                    <div className="feature">
                        <div className="feature-icon"></div>
                        <div className="feature-text">Connect your email and convert newsletters to high-quality audio files</div>
                    </div>
                    <div className="feature">
                        <div className="feature-icon"></div>
                        <div className="feature-text">Listen to your favorite content on the go, hands-free</div>
                    </div>
                    <div className="feature">
                        <div className="feature-icon"></div>
                        <div className="feature-text">Save time and stay informed while driving, exercising, or multitasking</div>
                    </div>
                </div>
                <GoogleButton />
            </div>
            <Footer />
        </div>
    );
}

export default Landing