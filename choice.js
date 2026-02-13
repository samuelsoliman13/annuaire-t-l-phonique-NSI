const messageArea = document.getElementById('message-area');

let messageTimeout;

function displayMessage(messageText, isError = false) {
    clearTimeout(messageTimeout); // Clear any existing timeout
    messageArea.textContent = messageText;
    messageArea.style.color = isError ? 'red' : 'green'; // Use green for success messages if any
    messageArea.style.display = 'block'; // Ensure it's visible

    messageTimeout = setTimeout(() => {
        messageArea.textContent = '';
        messageArea.style.display = 'none';
    }, 5000); // Message disappears after 5 seconds
}

document.getElementById('local-db').addEventListener('click', () => {
    const remember = document.getElementById('remember-choice').checked;
    window.ipc.send('db-choice', { type: 'local', remember });
});

document.getElementById('theo-server-db').addEventListener('click', async () => {
    const url = 'https://annuaire.dlchost.com';
    const remember = document.getElementById('remember-choice').checked;
    const theoServerButton = document.getElementById('theo-server-db');
    const originalButtonText = theoServerButton.textContent;

    // Clear any previous messages
    displayMessage('');

    // Show loading state
    theoServerButton.disabled = true;
    theoServerButton.textContent = 'Connecting...';

    const isReachable = await window.ipc.ping(url);

    // Restore button state
    theoServerButton.disabled = false;
    theoServerButton.textContent = originalButtonText;

    if (isReachable) {
        window.ipc.send('db-choice', { type: 'remote', url: url, remember });
    } else {
        displayMessage('Could not connect to Théo\'s server. Please ensure the server is running.', true);
    }
});

document.getElementById('remote-db').addEventListener('click', async () => {
    const urlInput = document.getElementById('remote-url');
    const url = urlInput.value;
    const remember = document.getElementById('remember-choice').checked;
    const remoteDbButton = document.getElementById('remote-db');
    const originalButtonText = remoteDbButton.textContent;

    // Clear any previous messages
    displayMessage('');

    if (!url) {
        displayMessage('Please enter a remote URL.', true);
        return;
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        displayMessage('Please enter a valid URL including http:// or https://', true);
        return;
    }

    // Show loading state
    remoteDbButton.disabled = true;
    remoteDbButton.textContent = 'Pinging...';

    const isReachable = await window.ipc.ping(url);

    // Restore button state
    remoteDbButton.disabled = false;
    remoteDbButton.textContent = originalButtonText;

    if (isReachable) {
        window.ipc.send('db-choice', { type: 'remote', url: url, remember });
    } else {
        displayMessage('Could not connect to the remote server. Please check the URL and ensure the server is running.', true);
    }
});
