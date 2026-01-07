# R00T_CAUSE Intelligence Feed

An automated cybersecurity news aggregation system designed for high-level research and security operations. This system utilizes RSS parsing and Discord Webhook integration to provide real-time updates on vulnerabilities, exploits, and industry breaches.

## Architecture and Design Principles

The project is built using Python 3.10 and adheres to SOLID design principles to ensure maintainability and scalability:

* **Single Responsibility:** Each module handles a distinct part of the pipeline (fetching, state management, or notification).
* **Dependency Inversion:** The core engine depends on abstractions, allowing for the easy integration of different notification platforms (e.g., Slack, Telegram) or data sources.
* **State Management:** Persistence is handled via a localized JSON state to prevent duplicate data transmission.

## Project Structure

* `main.py`: The entry point and orchestrator of the intelligence pipeline.
* `src/interfaces.py`: Defines abstract base classes for system components.
* `src/fetcher.py`: Manages RSS feed retrieval and XML parsing.
* `src/notifier.py`: Handles API interaction with Discord and data formatting.
* `src/state_manager.py`: Manages the tracking of previously processed intel.
* `.github/workflows/main.yml`: Configuration for automated execution via GitHub Actions.

## Installation and Deployment

## 1. Repository Setup

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## 2. Configuration

The system supports two methods of configuration:

* **Local:** Create a `.config.cfg` file following the INI format with a `[DISCORD]` section and `webhook_url` key.
* **Production (GitHub):** Define a Repository Secret named `DISCORD_WEBHOOK` containing the target Discord Webhook URL.

## 3. Automated Execution

The system is designed to run in a headless environment. The included GitHub Actions workflow is configured to trigger the pipeline every 60 minutes. It includes automated git-sync logic to update the `state.json` file, ensuring cross-session consistency.

## Usage

To execute the pipeline manually:

```bash
python main.py
```

## Security Considerations

The `.config.cfg` file and any local environment files should be excluded from version control via `.gitignore` to prevent credential leakage. When deploying via GitHub Actions, ensure the repository is set to private if the state file or logs contain sensitive organizational information.
