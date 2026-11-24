import re


def scan_dockerfile(content):
    findings = []

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    # Check 1: Running as root
    users = [
        line.split(maxsplit=1)[1].strip()
        for line in lines
        if line.upper().startswith("USER ")
    ]

    if not users or users[-1].lower().split(":")[0] in ("root", "0"):
        findings.append({
            "issue": "Possible root user execution",
            "severity": "HIGH",
            "recommendation": "Use a non-root user in the Dockerfile."
        })

    # Check 2: Using latest image tag
    for line in lines:
        if line.upper().startswith("FROM "):
            if re.search(r":latest(?:\s|$)", line, re.IGNORECASE):
                findings.append({
                    "issue": "Latest image tag detected",
                    "severity": "MEDIUM",
                    "recommendation": "Use a specific image version."
                })

    # Check 3: Potential hardcoded secrets
    for line in lines:
        if line.upper().startswith(("ENV ", "ARG ")):
            if re.search(
                r"(PASSWORD|SECRET|API_KEY|TOKEN)\s*=\s*\S+",
                line,
                re.IGNORECASE
            ):
                findings.append({
                    "issue": "Potential hardcoded secret",
                    "severity": "HIGH",
                    "recommendation": "Use a secure secrets manager."
                })

    return findings


def scan_terraform(content):
    findings = []

    # Check 1: Unrestricted network access
    if "0.0.0.0/0" in content or "::/0" in content:
        findings.append({
            "issue": "Unrestricted network access detected",
            "severity": "HIGH",
            "recommendation": "Restrict access to trusted IP ranges."
        })

    # Check 2: Potential hardcoded credentials
    if re.search(
        r'\b(password|secret_key|access_key|api_key|token)\s*=\s*"[^"]+"',
        content,
        re.IGNORECASE
    ):
        findings.append({
            "issue": "Potential hardcoded credentials",
            "severity": "HIGH",
            "recommendation": "Use secure variables or a secrets manager."
        })

    # Check 3: Encryption explicitly disabled
    if re.search(
        r"\bencrypted\s*=\s*false\b",
        content,
        re.IGNORECASE
    ):
        findings.append({
            "issue": "Encryption disabled",
            "severity": "HIGH",
            "recommendation": "Enable encryption to protect stored data."
        })

    return findings