<<<<<<< HEAD
# Contributing to Dart Vader

Thank you for your interest in contributing to Dart Vader.

Dart Vader is an open-source Discord bot designed to support Nerf and Humans vs Zombies (HvZ) communities through event management, attendance tracking, role management, and society administration tools.

Community contributions are welcome and appreciated. This document explains how to contribute effectively and help maintain the quality and reliability of the project.

---

# Before You Begin

Before contributing, please ensure that you have:

* Read the project's README.
* Read the Code of Conduct.
* Familiarised yourself with the project's goals and roadmap.
* Checked whether an issue already exists for the work you intend to perform.

---

# Types of Contributions

Contributions may include:

* Bug fixes
* New features
* Documentation improvements
* Refactoring and code quality improvements
* Test improvements
* Performance improvements
* User experience improvements

Contributors are encouraged to discuss significant changes before beginning implementation.

---

# Development Setup

## Clone the Repository

```bash
git clone <repository-url>
cd dart-vader
```

## Create a Virtual Environment

```bash
python -m venv venv
```

Linux:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create Environment Configuration

Copy the example configuration file:

```bash
cp .env.example .env
```

Populate the values required for your development environment.

---

# Project Structure

```text
dart-vader/
|-- assets/
|-- cogs/
|-- config/
|-- data/
|-- database/
|-- docs/
|-- logs/
|-- services/
|-- tests/
|-- utils/
|-- bot.py
`-- README.md
```

### Directory Responsibilities

| Directory | Purpose                                   |
| --------- | ----------------------------------------- |
| cogs      | Discord commands and interaction handlers |
| services  | Society and business logic                |
| database  | Database access and models                |
| tests     | Automated tests                           |
| utils     | Shared helper functionality               |
| docs      | Project documentation                     |
| config    | Configuration management                  |
| data      | Static data files                         |
| assets    | Images and project assets                 |

---

# Development Workflow

## Create or Select an Issue

Before beginning development, identify an existing issue or create a new one.

The issue should clearly describe:

* The problem
* Proposed solution
* Expected outcome

---

## Create a Feature Branch

Branch names should follow one of the following formats:

```text
feature/<feature-name>
bugfix/<issue-description>
docs/<documentation-change>
```

Examples:

```text
feature/event-signups
bugfix/attendance-recording
docs/readme-update
```

Create your branch from `develop`.

```bash
git checkout develop
git pull
git checkout -b feature/my-feature
```

---

## Implement Changes

While developing:

* Keep changes focused.
* Avoid unrelated modifications.
* Follow existing project conventions.
* Update documentation where necessary.
* Consider edge cases and error handling.

---

# Coding Standards

Contributors should aim to:

* Write clear and readable code.
* Use descriptive names.
* Keep functions focused on a single responsibility.
* Avoid unnecessary complexity.
* Add comments where clarification is genuinely useful.

### Separation of Responsibilities

Discord-specific behaviour should remain in:

```text
cogs/
```

Business and society logic should remain in:

```text
services/
```

Database access should remain in:

```text
database/
```

Contributors should avoid mixing these responsibilities unnecessarily.

---

# Testing

All contributions should be tested before submission.

Where appropriate:

* Add new tests.
* Update existing tests.
* Verify existing functionality still works.

At a minimum, contributors should verify that:

* The bot starts successfully.
* New functionality behaves as expected.
* Existing functionality has not been broken.
* No unexpected errors are generated.

---

# Documentation

Documentation should be updated whenever changes affect:

* User-facing functionality
* Configuration
* Deployment
* Development workflows

Relevant files may include:

* README.md
* ROADMAP.md
* User guides
* Governance documentation

---

# Commit Messages

Commit messages should clearly describe the change.

Good examples:

```text
Add event signup command

Fix attendance database query

Update FAQ documentation

Improve event validation logic
```

Avoid messages such as:

```text
fix

update

changes

stuff
```

---

# Pull Requests

All changes should be submitted through a Pull Request targeting the `develop` branch.

Each Pull Request should include:

## Summary

A brief explanation of the change.

## Motivation

Why the change is required.

## Testing

A description of testing performed.

## Related Issues

References to any associated GitHub issues.

---

# Review Process

Pull Requests are reviewed by project maintainers.

Reviewers may:

* Approve the contribution.
* Request modifications.
* Reject the contribution.

Approval is based on:

* Functionality
* Reliability
* Security
* Maintainability
* Documentation quality
* Alignment with project goals

---

# Security

If you discover a security vulnerability, please do not open a public issue.

Instead, follow the process described in:

```text
SECURITY.md
```

---

# Questions and Support

If you are unsure about any aspect of the contribution process, please open a discussion or contact a maintainer before proceeding.

We appreciate all contributions and thank you for helping improve Dart Vader.
=======
# Contributing to Dart Vader

Thank you for your interest in contributing to Dart Vader.

Dart Vader is an open-source Discord bot designed to support Nerf and Humans vs Zombies (HvZ) communities through event management, attendance tracking, role management, and society administration tools.

Community contributions are welcome and appreciated. This document explains how to contribute effectively and help maintain the quality and reliability of the project.

---

# Before You Begin

Before contributing, please ensure that you have:

* Read the project's README.
* Read the Code of Conduct.
* Familiarised yourself with the project's goals and roadmap.
* Checked whether an issue already exists for the work you intend to perform.

---

# Types of Contributions

Contributions may include:

* Bug fixes
* New features
* Documentation improvements
* Refactoring and code quality improvements
* Test improvements
* Performance improvements
* User experience improvements

Contributors are encouraged to discuss significant changes before beginning implementation.

---

# Development Setup

## Clone the Repository

```bash
git clone <repository-url>
cd dart-vader
```

## Create a Virtual Environment

```bash
python -m venv venv
```

Linux:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create Environment Configuration

Copy the example configuration file:

```bash
cp .env.example .env
```

Populate the values required for your development environment.

---

# Project Structure

```text
dart-vader/
|-- assets/
|-- cogs/
|-- config/
|-- data/
|-- database/
|-- docs/
|-- logs/
|-- services/
|-- tests/
|-- utils/
|-- bot.py
`-- README.md
```

### Directory Responsibilities

| Directory | Purpose                                   |
| --------- | ----------------------------------------- |
| cogs      | Discord commands and interaction handlers |
| services  | Society and business logic                |
| database  | Database access and models                |
| tests     | Automated tests                           |
| utils     | Shared helper functionality               |
| docs      | Project documentation                     |
| config    | Configuration management                  |
| data      | Static data files                         |
| assets    | Images and project assets                 |

---

# Development Workflow

## Create or Select an Issue

Before beginning development, identify an existing issue or create a new one.

The issue should clearly describe:

* The problem
* Proposed solution
* Expected outcome

---

## Create a Feature Branch

Branch names should follow one of the following formats:

```text
feature/<feature-name>
bugfix/<issue-description>
docs/<documentation-change>
```

Examples:

```text
feature/event-signups
bugfix/attendance-recording
docs/readme-update
```

Create your branch from `develop`.

```bash
git checkout develop
git pull
git checkout -b feature/my-feature
```

---

## Implement Changes

While developing:

* Keep changes focused.
* Avoid unrelated modifications.
* Follow existing project conventions.
* Update documentation where necessary.
* Consider edge cases and error handling.

---

# Coding Standards

Contributors should aim to:

* Write clear and readable code.
* Use descriptive names.
* Keep functions focused on a single responsibility.
* Avoid unnecessary complexity.
* Add comments where clarification is genuinely useful.

### Separation of Responsibilities

Discord-specific behaviour should remain in:

```text
cogs/
```

Business and society logic should remain in:

```text
services/
```

Database access should remain in:

```text
database/
```

Contributors should avoid mixing these responsibilities unnecessarily.

---

# Testing

All contributions should be tested before submission.

Where appropriate:

* Add new tests.
* Update existing tests.
* Verify existing functionality still works.

At a minimum, contributors should verify that:

* The bot starts successfully.
* New functionality behaves as expected.
* Existing functionality has not been broken.
* No unexpected errors are generated.

---

# Documentation

Documentation should be updated whenever changes affect:

* User-facing functionality
* Configuration
* Deployment
* Development workflows

Relevant files may include:

* README.md
* ROADMAP.md
* User guides
* Governance documentation

---

# Commit Messages

Commit messages should clearly describe the change.

Good examples:

```text
Add event signup command

Fix attendance database query

Update FAQ documentation

Improve event validation logic
```

Avoid messages such as:

```text
fix

update

changes

stuff
```

---

# Pull Requests

All changes should be submitted through a Pull Request targeting the `develop` branch.

Each Pull Request should include:

## Summary

A brief explanation of the change.

## Motivation

Why the change is required.

## Testing

A description of testing performed.

## Related Issues

References to any associated GitHub issues.

---

# Review Process

Pull Requests are reviewed by project maintainers.

Reviewers may:

* Approve the contribution.
* Request modifications.
* Reject the contribution.

Approval is based on:

* Functionality
* Reliability
* Security
* Maintainability
* Documentation quality
* Alignment with project goals

---

# Security

If you discover a security vulnerability, please do not open a public issue.

Instead, follow the process described in:

```text
SECURITY.md
```

---

# Questions and Support

If you are unsure about any aspect of the contribution process, please open a discussion or contact a maintainer before proceeding.

We appreciate all contributions and thank you for helping improve Dart Vader.
>>>>>>> 70ee258 (Connecting traspberry pi and fix minor version compatability issues)
