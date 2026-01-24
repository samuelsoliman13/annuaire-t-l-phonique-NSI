# GEMINI.md - Project Context for Annuaire Téléphonique

## Project Overview

This project is a desktop contact management application built using **Electron**, **Node.js**, and a **Python Flask** backend. It allows users to add, edit, delete, and search for contacts. A key feature is the ability to choose between using a local SQLite database (with a spawned Python Flask server) or connecting to a remote Flask API. A separate Python command-line interface (CLI) is also provided for direct interaction with the contact management system.

## Main Technologies

*   **Frontend:**
    *   **Electron:** Desktop application framework.
    *   **Node.js:** Runtime environment for Electron.
    *   **HTML, CSS, JavaScript:** For the user interface.
    *   **electron-store:** For persisting user preferences (e.g., database choice).
*   **Backend:**
    *   **Python Flask:** Web framework for the RESTful API.
    *   **Flask-CORS:** Handles Cross-Origin Resource Sharing for API calls.
    *   **Flask-SQLAlchemy:** ORM for database interactions.
    *   **SQLite:** Default local database.

## Architecture

The application follows a client-server architecture within the Electron wrapper:

*   **Electron Main Process (`main.js`):**
    *   Manages the lifecycle of application windows (`choiceWindow`, `mainWindow`).
    *   Spawns the Python Flask backend (`api.py`) as a child process if the "local database" option is selected.
    *   Handles Inter-Process Communication (IPC) for events like database choice (`db-choice`) and forgetting preferences (`forget-db-choice`).
    *   Persists the user's database choice using `electron-store`.
    *   Initializes the database connection by sending a POST request to `/api/init-db` on the Flask server.
*   **Electron Renderer Processes (`index.js`, `choice.js`):**
    *   `choice.js`: Manages the initial database selection interface (local vs. remote API, remember choice).
    *   `index.js`: Implements the main contact management UI, handling CRUD operations (add, edit, delete, search).
    *   Both communicate with the Electron main process via `window.ipc.send` and with the backend API via a custom `window.api.fetch` (exposed by the preload script).
*   **Electron Preload Script (`preload.js`):**
    *   Securely exposes an `api` object (for custom `fetch` and IPC event handling) and an `ipc` object (for sending messages) to the renderer processes, bridging the Node.js context with the web page.
*   **Python Flask Backend (`api.py`):**
    *   A RESTful API providing endpoints for contact management (GET, POST, PUT, DELETE contacts), search, and statistics.
    *   The `AnnuaireManager` class encapsulates the core business logic for database operations.
    *   The `/api/init-db` endpoint is crucial for dynamically configuring the database URI based on user choice.
*   **Python CLI (`cli.py`):**
    *   A standalone command-line interface that reuses the `AnnuaireManager` logic for direct, text-based contact management. It provides an alternative way to interact with the contact system, separate from the Electron GUI.

## Building and Running

### Prerequisites

*   Node.js and npm
*   Python 3 and pip

### Installation

1.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Electron Application

To start the desktop application:

```bash
npm start
```

Upon launch, you will be prompted to choose your database preference:
*   **Local Database:** A Python Flask server will be automatically started in the background, using a local SQLite database (`contacts.db` in Electron's user data path).
*   **Remote Database:** You will need to provide the URL of an existing, compatible Flask API server.

### Running the Python CLI (Optional, separate from Electron)

To use the command-line interface for contact management:

```bash
python cli.py
```
*(Note: Ensure that the `AnnuaireManager` class from `api.py` is correctly imported and available to `cli.py`. If running `cli.py` directly, it will default to using a local `contacts.db` in the current working directory unless explicitly configured otherwise within its execution context.)*

## Development Conventions

*   **Separation of Concerns:** Clear distinction between frontend (Electron, JavaScript, HTML, CSS) and backend (Python Flask) logic.
*   **IPC for Electron:** Utilizes Electron's IPC mechanisms for secure and structured communication between the main and renderer processes.
*   **Modular Backend:** The `AnnuaireManager` class centralizes database operations in the Python backend, promoting reusability and maintainability.
*   **Dynamic Database Configuration:** The backend supports dynamic database URI configuration via an API endpoint, allowing flexibility in deployment.
