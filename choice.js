document.getElementById('local-db').addEventListener('click', () => {
    const remember = document.getElementById('remember-choice').checked;
    window.ipc.send('db-choice', { type: 'local', remember });
});

document.getElementById('remote-db').addEventListener('click', () => {
    const url = document.getElementById('remote-url').value;
    const remember = document.getElementById('remember-choice').checked;
    if (url) {
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            alert('Please enter a valid URL including http:// or https://');
            return;
        }
        window.ipc.send('db-choice', { type: 'remote', url: url, remember });
    } else {
        alert('Please enter a remote URL.');
    }
});
