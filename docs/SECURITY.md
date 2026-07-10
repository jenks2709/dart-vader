# Security Policy

## Purpose

The Dart Vader project takes security seriously and appreciates the efforts of individuals who responsibly identify and report vulnerabilities.

This document explains how to report security issues and how security reports will be handled.

---

# Supported Versions

Security fixes are only guaranteed for the most recent stable release of Dart Vader.

| Version               | Supported |
| --------------------- | --------- |
| Latest Stable Release | ✓         |
| Previous Releases     | ✗         |
| Development Builds    | ✗         |

Users are encouraged to upgrade to the latest stable version whenever possible.

---

# Reporting a Vulnerability

If you discover a potential security vulnerability, please do **not** create a public GitHub issue.

Public disclosure before a fix is available may place users of the project at unnecessary risk.

Instead, contact the project maintainers privately and provide:

* A description of the vulnerability.
* Steps required to reproduce the issue.
* The affected version(s).
* Any supporting screenshots, logs, or proof-of-concept material.
* Any suggested mitigations or fixes, if available.

Reports should contain sufficient detail to allow the issue to be reproduced and verified.

---

# What to Report

Examples of security-related issues include:

* Authentication bypasses.
* Permission escalation vulnerabilities.
* Command execution vulnerabilities.
* Sensitive data exposure.
* Token or credential leakage.
* Database security issues.
* Input validation failures.
* Vulnerabilities introduced through project dependencies.
* Denial-of-service vulnerabilities.
* Any behaviour that could allow unauthorised access or abuse.

If you are unsure whether an issue is security-related, please report it.

---

# What Not to Report

The following are generally not considered security vulnerabilities:

* Minor user interface issues.
* Feature requests.
* Documentation errors.
* Formatting issues.
* Suggestions for non-security improvements.
* Issues requiring unrealistic or highly privileged access to exploit.

These should be reported through the normal issue tracking process.

---

# Responsible Disclosure

Contributors and researchers are expected to follow responsible disclosure practices.

Please:

* Allow maintainers reasonable time to investigate and address reported vulnerabilities.
* Avoid public disclosure before a fix is available.
* Avoid accessing, modifying, or deleting data that does not belong to you.
* Avoid actions that may negatively impact users, servers, or communities using Dart Vader.

The goal of security research should be to improve the security of the project, not to disrupt its operation.

---

# Security Response Process

When a report is received, maintainers will attempt to:

1. Acknowledge receipt of the report.
2. Assess the validity and severity of the issue.
3. Investigate the affected components.
4. Develop and test a fix where appropriate.
5. Release a patched version if necessary.
6. Publish information about the issue after remediation, where appropriate.

Response times may vary depending on maintainer availability and the complexity of the issue.

---

# Dependency Security

Dart Vader relies on third-party software libraries.

Maintainers will make reasonable efforts to:

* Monitor dependency vulnerabilities.
* Keep dependencies reasonably up to date.
* Apply security updates where appropriate.
* Remove unsupported or insecure dependencies when necessary.

Contributors are encouraged to report known dependency vulnerabilities.

---

# Security Best Practices for Deployments

Operators deploying Dart Vader should:

* Keep the bot updated.
* Protect Discord bot tokens.
* Never commit secrets to source control.
* Restrict bot permissions to the minimum required.
* Regularly review server permissions.
* Monitor logs for unexpected behaviour.
* Keep host operating systems updated.

---

# Scope

This policy applies to:

* The Dart Vader source code.
* Official releases.
* Project documentation.
* Configuration examples provided by the project.

Third-party deployments and modifications are outside the direct control of the maintainers.

---

# Acknowledgements

The Dart Vader project appreciates responsible security research and values individuals who help improve the security and reliability of the software through constructive reporting and collaboration.
