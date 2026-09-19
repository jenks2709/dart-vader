# Dart Vader

> *"I find your lack of eye protection disturbing."*

Dart Vader is an open-source Discord bot designed to support Nerf and Humans versus Zombies (HvZ) communities through event management, attendance tracking, role management, and society administration tools.

The project aims to reduce administrative workload for organisers while improving the experience of players and society members.

---

## Features

### Event Management

* Create and manage events
* Event sign-ups and withdrawals
* Event rosters
* Event reminders
* Event information commands

### Society Administration

* FAQ system
* Rules and information commands
* Committee contact information
* Administrative announcements

### Role Management

* Self-assigned community roles
* Role removal
* Role listings

### Attendance Tracking

* Attendance recording
* Attendance history
* Basic participation statistics

### Community Features

* Quotes
* Fun commands
* Community engagement tools

---

## Project Status

**Current Version:** 1.0 (In Development)

Dart Vader is currently under active development. The Version 1.0 release focuses on providing a stable and maintainable foundation for future community-driven development.

---

## Project Philosophy

Dart Vader is intended to be:

* Reliable
* Maintainable
* Extensible
* Community-driven
* Easy to deploy
* Easy to contribute to

The project prioritises stability, security, and usability over rapid feature growth.

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd dart-vader
```

### Create a Virtual Environment

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

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Copy the example configuration file:

```bash
cp .env.example .env
```

Populate the required values.

### Run the Bot

```bash
python bot.py
```

---

## Configuration

Dart Vader uses environment variables for configuration.

Example:

```env
DISCORD_TOKEN=
GUILD_ID=

ANNOUNCEMENT_CHANNEL_ID=
EVENT_CHANNEL_ID=
LOG_CHANNEL_ID=

COMMITTEE_ROLE_ID=
ADMIN_ROLE_ID=

DATABASE_PATH=database/dart_vader.db

LOG_LEVEL=INFO

TIMEZONE=Europe/London
```

Refer to `.env.example` for the full configuration template.

---

## Project Structure

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

### Directory Overview

| Directory | Purpose                                   |
| --------- | ----------------------------------------- |
| cogs      | Discord commands and interaction handlers |
| services  | Society and business logic                |
| database  | Database models and persistence           |
| tests     | Automated tests (to be added)             |
| utils     | Shared helper functionality               |
| config    | Configuration management                  |
| data      | Static project data                       |
| docs      | Documentation                             |
| assets    | Images and project assets                 |
| logs      | Runtime logs                              |

---

## Documentation

### Governance

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)
* [Security Policy](SECURITY.md)
* [Maintainers Guide](MAINTAINERS.md)

### Project Planning

* [Project Roadmap](ROADMAP.md)

---

## Development Workflow

Development follows a maintainer-led workflow.

```text
feature/*
    ↓
Pull Request
    ↓
Review
    ↓
develop
    ↓
Release
    ↓
main
```

Direct commits to the `main` branch are not permitted.

---

## Contributing

Community contributions are welcome.

Please read:

1. [Contributing Guide](CONTRIBUTING.md)
2. [Code of Conduct](CODE_OF_CONDUCT.md)

before submitting changes.

---

## Security

If you discover a security vulnerability, please do not create a public issue.

Refer to:

[SECURITY.md](SECURITY.md)

for information on responsible disclosure.

---

## Relationship to Tagger

Dart Vader and Tagger serve different purposes.

### Dart Vader

Society management:

* Events
* Attendance
* Roles
* Administration
* Community tools

### Tagger

Humans versus Zombies gameplay:

* Player registration
* Infection tracking
* Missions
* Gameplay systems

This separation allows each project to remain focused on its intended purpose.

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## Maintainers

Current lead maintainer:

**Alec Jenkins**

See [MAINTAINERS.md](MAINTAINERS.md) for project governance and maintainer responsibilities.

---

## Acknowledgements

Dart Vader is developed for the Nerf and Humans versus Zombies community and is intended to support organisers, players, and volunteers who help run events and societies.
