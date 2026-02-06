document.getElementById('local-db').addEventListener('click', () => {
    const remember = document.getElementById('remember-choice').checked;
    window.ipc.send('db-choice', { type: 'local', remember });
});

document.getElementById('remote-db').addEventListener('click', async () => {
    const urlInput = document.getElementById('remote-url');
    const url = urlInput.value;
    const remember = document.getElementById('remember-choice').checked;
    const remoteDbButton = document.getElementById('remote-db');
    const originalButtonText = remoteDbButton.textContent;

    if (!url) {
        alert('Please enter a remote URL.');
        return;
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        alert('Please enter a valid URL including http:// or https://');
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
        alert('Could not connect to the remote server. Please check the URL and ensure the server is running.');
    }
});
