import { useState, useEffect, useCallback, useRef } from "react";
import {
  checkHealth,
  getSummary,
  getScans,
  getScanDetails,
  uploadFile,
  updateScan,
  deleteScan,
} from "./api";
import "./App.css";

function App() {
  const [connected, setConnected] = useState(false);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [result, setResult] = useState(null);
  const [scans, setScans] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [historyError, setHistoryError] = useState("");
  const [busy, setBusy] = useState(false);
  const [summary, setSummary] = useState({
    total_scans: 0,
    total_findings: 0,
    high_risk: 0,
    medium_risk: 0,
  });

  const fileInput = useRef(null);
  const submitting = useRef(false);

  // Fetch dashboard data from backend
  const refreshDashboard = useCallback(async () => {
    setHistoryLoading(true);
    setHistoryError("");

    try {
      const health = await checkHealth();
      setConnected(health.status === "healthy");

      const [summaryData, scanData] = await Promise.all([
        getSummary(),
        getScans(),
      ]);

      setSummary(summaryData);
      setScans(scanData.scans || []);
    } catch {
      setHistoryError(
        "Unable to load dashboard data. Check the backend connection."
      );
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshDashboard();
  }, [refreshDashboard]);

  // Handle file selection
  function handleFileChange(event) {
    setFile(event.target.files[0] || null);
    setError("");
    setSuccess("");
  }

  // Upload and scan configuration file
  async function handleUpload(event) {
    event.preventDefault();

    if (submitting.current) return;

    setError("");
    setSuccess("");

    if (!file) {
      setError("Please select a configuration file.");
      return;
    }

    const filename = file.name.toLowerCase();

    if (
      filename !== "dockerfile" &&
      !filename.endsWith(".tf")
    ) {
      setError("Only Dockerfile and Terraform (.tf) files are supported.");
      return;
    }

    if (file.size === 0) {
      setError("The selected file is empty.");
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      setError("File size must not exceed 2 MB.");
      return;
    }

    submitting.current = true;
    setLoading(true);
    setResult(null);

    try {
      const data = await uploadFile(file);

      setResult({
        id: data.scan_id,
        filename: data.original_filename,
        file_type: data.file_type,
        ...data.security_scan,
      });

      setSuccess("Security scan completed and saved successfully!");
      setFile(null);

      if (fileInput.current) {
        fileInput.current.value = "";
      }

      await refreshDashboard();
    } catch (err) {
      setError(err.message || "Unable to complete the scan.");
    } finally {
      setLoading(false);
      submitting.current = false;
    }
  }

  // View a previous scan
  async function handleView(id) {
    setError("");
    setSuccess("");
    setBusy(true);

    try {
      const data = await getScanDetails(id);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  // Rename a scan record
  async function handleRename(scan) {
    const filename = window.prompt(
      "Enter a new display name:",
      scan.filename
    );

    if (filename === null) return;

    if (!filename.trim()) {
      setError("Filename cannot be empty.");
      return;
    }

    setError("");
    setSuccess("");
    setBusy(true);

    try {
      await updateScan(scan.id, filename.trim());

      setResult((previous) =>
        previous?.id === scan.id
          ? { ...previous, filename: filename.trim() }
          : previous
      );

      setSuccess("Scan record updated successfully.");
      await refreshDashboard();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  // Delete a scan record
  async function handleDelete(id) {
    const confirmed = window.confirm(
      "Delete this scan report from the database?"
    );

    if (!confirmed) return;

    setError("");
    setSuccess("");
    setBusy(true);

    try {
      await deleteScan(id);

      setResult((previous) =>
        previous?.id === id ? null : previous
      );

      setSuccess("Scan record deleted successfully.");
      await refreshDashboard();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="dashboard">
      <header className="header">
        <div>
          <p className="eyebrow">INFRASTRUCTURE SECURITY</p>
          <h1>InfraSentry <span>AI</span></h1>
          <p className="subtitle">
            Infrastructure Security Intelligence Platform
          </p>
        </div>

        <div className={`status ${connected ? "online" : "offline"}`}>
          <span className="status-dot"></span>
          {connected ? "Backend Connected" : "Connection Unverified"}
        </div>
      </header>

      <main>
        <div className="section-heading">
          <h2>Security Overview</h2>
          <button
            className="secondary-button"
            onClick={refreshDashboard}
            disabled={historyLoading || loading || busy}
          >
            Refresh
          </button>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <p>Total Scans</p>
            <h2>{summary.total_scans}</h2>
          </div>

          <div className="stat-card">
            <p>Total Findings</p>
            <h2>{summary.total_findings}</h2>
          </div>

          <div className="stat-card high">
            <p>High Risk</p>
            <h2>{summary.high_risk}</h2>
          </div>

          <div className="stat-card medium">
            <p>Medium Risk</p>
            <h2>{summary.medium_risk}</h2>
          </div>
        </div>

        <section className="panel">
          <h2>New Security Scan</h2>
          <p className="muted">
            Upload a Dockerfile or Terraform configuration
            to identify potential security issues.
          </p>

          <form onSubmit={handleUpload}>
            <div className="upload-area">
              <h3>Upload Configuration</h3>
              <p>Dockerfile or .tf • Maximum 2 MB</p>

              <input
                ref={fileInput}
                type="file"
                onChange={handleFileChange}
                disabled={loading || busy}
              />

              {file && (
                <p className="selected-file">
                  Selected: {file.name}
                </p>
              )}
            </div>

            <button
              className="primary-button"
              type="submit"
              disabled={loading || busy}
            >
              {loading ? "Analyzing configuration..." : "Run Security Scan"}
            </button>
          </form>

          {error && (
            <div className="message error" role="alert">
              {error}
            </div>
          )}

          {success && (
            <div className="message success" role="status">
              {success}
            </div>
          )}
        </section>

        {result && (
          <section className="panel">
            <div className="section-heading">
              <h2>Security Scan Report</h2>
              <button
                className="secondary-button"
                onClick={() => setResult(null)}
              >
                Close
              </button>
            </div>

            <p className="muted">
              Scan #{result.id} — {result.filename}
            </p>

            <div className="result-summary">
              <span>Type: {result.file_type}</span>
              <span>Findings: {result.total_findings}</span>
              <span className="high-text">
                High: {result.high_risk}
              </span>
              <span className="medium-text">
                Medium: {result.medium_risk}
              </span>
            </div>

            {(result.findings || []).length === 0 ? (
              <div className="message success">
                No issues detected by the current security rules.
              </div>
            ) : (
              result.findings.map((finding, index) => (
                <div className="finding-card" key={index}>
                  <span
                    className={`severity ${finding.severity.toLowerCase()}`}
                  >
                    {finding.severity}
                  </span>

                  <h3>{finding.issue}</h3>

                  <p>
                    <strong>Recommendation:</strong>{" "}
                    {finding.recommendation}
                  </p>
                </div>
              ))
            )}
          </section>
        )}

        <section className="panel">
          <h2>Scan History</h2>
          <p className="muted">
            Previous security reports stored in the database.
          </p>

          {historyLoading ? (
            <p>Loading scan history...</p>
          ) : historyError ? (
            <div className="message error">
              {historyError}
            </div>
          ) : scans.length === 0 ? (
            <div className="empty-state">
              No scans available. Upload a configuration
              file to get started.
            </div>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Filename</th>
                    <th>Type</th>
                    <th>Findings</th>
                    <th>High</th>
                    <th>Medium</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>
                  {scans.map((scan) => (
                    <tr key={scan.id}>
                      <td>#{scan.id}</td>
                      <td>{scan.filename}</td>
                      <td>{scan.file_type}</td>
                      <td>{scan.total_findings}</td>
                      <td className="high-text">
                        {scan.high_risk}
                      </td>
                      <td className="medium-text">
                        {scan.medium_risk}
                      </td>
                      <td className="actions">
                        <button
                          disabled={busy || loading}
                          onClick={() => handleView(scan.id)}
                        >
                          View
                        </button>

                        <button
                          disabled={busy || loading}
                          onClick={() => handleRename(scan)}
                        >
                          Rename
                        </button>

                        <button
                          className="delete-button"
                          disabled={busy || loading}
                          onClick={() => handleDelete(scan.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>

      <footer>
        InfraSentry AI © 2026 | Infrastructure Security Intelligence
      </footer>
    </div>
  );
}

export default App;