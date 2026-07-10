# Maintainers Guide

## Purpose

This document defines the responsibilities, authority, and expectations of Dart Vader maintainers.

Its purpose is to ensure that the project can be managed consistently over time and that future maintainers understand how the project is intended to operate.

---

# Current Maintainers

## Lead Maintainer

**AJ Jenkins**

### Responsibilities

* Review and approve Pull Requests.
* Manage releases.
* Maintain project documentation.
* Define project priorities.
* Manage repository settings.
* Enforce project governance policies.
* Appoint additional maintainers when required.

---

# Project Governance Model

Dart Vader follows a **maintainer-led governance model**.

Community contributions are encouraged, but maintainers retain final authority regarding:

* Code acceptance.
* Release scheduling.
* Project direction.
* Technical standards.
* Security decisions.
* Governance policies.

Contributions are evaluated on their technical merit, maintainability, reliability, security, and alignment with project goals.

---

# Maintainer Responsibilities

Maintainers are expected to:

* Act professionally and respectfully.
* Review contributions fairly and consistently.
* Prioritise project stability and security.
* Maintain documentation accuracy.
* Encourage constructive community participation.
* Respond to issues and Pull Requests within a reasonable timeframe where possible.

Maintainers should seek to support contributors while preserving the quality and long-term maintainability of the project.

---

# Pull Request Review Standards

Before approving a Pull Request, maintainers should verify that:

* The proposed change functions correctly.
* Existing functionality is not negatively affected.
* Appropriate testing has been performed.
* Documentation has been updated where necessary.
* Security implications have been considered.
* The change aligns with project goals.

Maintainers may request modifications before approval.

---

# Approval Requirements

A Pull Request may be merged when:

* Review has been completed.
* Requested changes have been addressed.
* No unresolved discussions remain.
* Documentation requirements have been satisfied.
* A maintainer has granted approval.

For the current maintainer-led model, a single maintainer approval is sufficient.

Future governance models may require multiple approvals.

---

# Branch Strategy

The project uses the following branch structure:

```text
main
└── Production-ready code

develop
└── Integration and testing branch

feature/*
└── Individual feature development
```

## Main Branch

The `main` branch should contain only stable, release-ready code.

Direct commits to `main` are prohibited.

Changes should reach `main` only through the approved review process.

## Develop Branch

The `develop` branch is used for integration and testing of approved changes prior to release.

## Feature Branches

Contributors should perform development within dedicated feature branches.

Examples:

```text
feature/event-signups
feature/attendance-system
feature/reminder-service
```

---

# Release Management

Maintainers are responsible for coordinating releases.

Prior to release, maintainers should verify:

* Planned functionality is complete.
* Critical defects have been addressed.
* Documentation is current.
* Testing has been completed successfully.

Release process:

1. Merge approved changes into `develop`.
2. Complete final testing.
3. Merge `develop` into `main`.
4. Create a version tag.
5. Publish release notes.
6. Deploy the release.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

# Security Responsibilities

Maintainers are responsible for:

* Reviewing security reports.
* Investigating reported vulnerabilities.
* Coordinating security fixes.
* Publishing security updates when required.

Security issues should be handled according to the procedures defined in:

```text
SECURITY.md
```

---

# Documentation Responsibilities

Maintainers should ensure that documentation remains accurate and up to date.

Documentation requiring regular review includes:

* README.md
* ROADMAP.md
* CONTRIBUTING.md
* SECURITY.md
* CODE_OF_CONDUCT.md
* This document

Documentation should be updated alongside relevant code changes whenever practical.

---

# Adding New Maintainers

Additional maintainers may be appointed when:

* The project workload increases significantly.
* Sustained contributions demonstrate technical competence.
* Additional review capacity is required.
* Long-term project continuity would benefit from shared responsibility.

New maintainers should:

* Demonstrate familiarity with the project.
* Understand the governance model.
* Be willing to participate in reviews and releases.
* Act in accordance with project policies.

---

# Removing Maintainers

Maintainer status may be revoked when:

* A maintainer voluntarily steps down.
* A maintainer becomes inactive for an extended period.
* A maintainer repeatedly fails to fulfil responsibilities.
* A maintainer acts contrary to project policies.

The lead maintainer retains authority regarding maintainer appointments and removals.

---

# Succession Planning

If the lead maintainer is no longer able to maintain the project, responsibility should pass to an active maintainer who:

* Understands the project architecture.
* Has demonstrated sound judgement.
* Has a history of constructive contributions.
* Is willing to assume long-term responsibility for the project.

The objective is to ensure continuity of development and support for the community.

---

# Guiding Principle

Maintainers should prioritise:

> Stability, security, maintainability, and community benefit over rapid feature development.

Dart Vader exists to support Nerf and Humans versus Zombies communities. All project decisions should be made with the long-term health of the software and its users in mind.
