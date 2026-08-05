<!--
File: SECURITY.md
Project: NeuroFlow AI
-->

# Security Policy

NeuroFlow AI is an enterprise-grade modular AI platform designed for mission-critical intelligent orchestrations. Security, data privacy, and isolation are core priorities for our platform architecture.

---

## Supported Versions

Only active development baselines and released platform versions receive security updates and patches.

| Version | Supported | Security Maintenance |
| :--- | :--- | :--- |
| `0.1.x` (Main / Active Dev) | Yes | Active vulnerability patching |
| `< 0.1.0` | No | Deprecated development snapshots |

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public issue trackers.**

Security contact information will be published before the first public release. In the interim, confidential security disclosures should be directed through private repository channels or security maintainers.

### What to Include in Your Report
To assist in triage and rapid response, reports should include:
- A clear summary of the vulnerability.
- Steps to reproduce the issue (including proof-of-concept scripts or payload examples where applicable).
- Affected platform components (e.g., Agent Runtime, Tool Runtime execution context, Integration transport, API authentication).
- Potential impact (e.g., Remote Code Execution, Privilege Escalation, Multi-Tenant Data Leakage).
- Any proposed mitigations or fix recommendations.

---

## Response & Disclosure Process SLA

When a security vulnerability is reported, the security team adheres to the following SLA:

1. **Initial Acknowledgment (within 48 hours):** Receipt of the report is confirmed and a primary security coordinator is assigned.
2. **Triage & Validation (within 5 business days):** The report is investigated, severity assessed (CVSS v3.1 score), and actionability confirmed.
3. **Remediation & Patching:** A security patch is developed and verified in a private repository branch.
4. **Coordinated Disclosure (90-day Embargo):** Public disclosure is coordinated alongside the patched release. Reporters are requested to maintain confidentiality during the 90-day window or until the patch is published.

---

## Security Architectural Guarantees

NeuroFlow AI enforces key security properties at the architectural level:
- **Tool Sandbox Execution:** Tool executions undergo validation and operate within bounded, unprivileged execution contexts.
- **Tenant Isolation:** Multi-tenant deployments enforce strict queue, vector namespace, and database row-level isolation.
- **Secrets Management:** Infrastructure credentials (API keys, connection strings) are loaded via environment variables or secret management services; raw secrets are prohibited in code or configuration files.
- **Layer Boundary Enforcement:** API Ingress cannot bypass Layer 3 execution governance or directly manipulate Layer 0/1 infrastructure contracts.
