# Annuaire Téléphonique

This is a simple contact management application built with Electron, Node.js, and Python.

## Features

- Add, edit, and delete contacts.
- Search for contacts.
- Choose between a local and a remote database.

## How to run the application

1.  **Install the dependencies:**
    ```
    npm install
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```
    npm start
    ```

## How to use the application

When you start the application, you will be prompted to choose between a local and a remote database.

-   **Use Local Database:**
    -   The application will start a local server and use a local `contacts.json` file.
-   **Use Remote Database:**
    -   You will need to provide the URL of a remote API. The application will then use this remote API to fetch and manage the contacts.
    -   The remote API must be compatible with the API defined in `api.py`.
