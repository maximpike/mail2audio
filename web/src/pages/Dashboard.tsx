import "../App.css"
import "../styles/Dashboard.css"

function Dashboard() {
    return (
        <div className="page-container">
            <div className="dashboard-container">
                {/*//Header*/}
                <div className="dashboard-header">
                    <h1 className="dashboard-title">📧 Mail2Audio Dashboard</h1>
                </div>

                {/*Upload Section*/}
                <div className="upload-section">
                    <div className="upload-zone" id="uploadZone">
                        <div className="upload-icon">📤</div>
                        <div className="upload-text">Drop your .eml file here or click to browse</div>
                        <div className="upload-hint">Only .eml files are supported</div>
                        <input type="file" id="fileInput" className="file-input" accept=".eml"/>
                    </div>
                    <div id="uploadStatus"></div>
                </div>

                {/*Email List*/}
                <div className="email-list">
                    <h2 className="email-list-header">Your Emails</h2>
                    <div id="emaillistContainer">
                        <div className="spinner"></div>
                    </div>
                </div>

            </div>
        </div>
    );

}

export default Dashboard