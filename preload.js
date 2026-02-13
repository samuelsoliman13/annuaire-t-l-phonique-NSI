const { contextBridge, ipcRenderer } = require('electron');

let dbUrl;

ipcRenderer.on('db-url', (event, url) => {
  console.log('Preload received db-url:', url);
  dbUrl = url;
});

contextBridge.exposeInMainWorld('api', {
  getDbUrl: () => dbUrl,
  fetch: (url, options) => {
    if (!dbUrl) {
      console.error('Database URL not set!');
      return Promise.reject('Database URL not set');
    }
    const fullUrl = `${dbUrl}${url}`;
    console.log(`Fetching from: ${fullUrl}`);
    return fetch(fullUrl, options)
      .then(res => {
        return res.json().then(data => {
          if (!res.ok) {
            console.error(`HTTP Error: ${res.status} ${res.statusText}`, data);
            // Si le serveur retourne un objet avec "erreur", utiliser ce message
            const errorMsg = data.erreur || `HTTP ${res.status}: ${res.statusText}`;
            throw new Error(errorMsg);
          }
          return data;
        });
      })
      .catch(err => {
        console.error(`Fetch error: ${err.message}`);
        throw err;
      });
  },
  on: (channel, callback) => {
    // Passer les arguments de l'événement au callback
    ipcRenderer.on(channel, (event, ...args) => callback(...args));
  },
  forgetDbChoice: () => {
    ipcRenderer.send('forget-db-choice');
  }
});

contextBridge.exposeInMainWorld('ipc', {
  send: (channel, data) => {
    ipcRenderer.send(channel, data);
  },
  ping: async (url) => {
    return await ipcRenderer.invoke('ping-url', url);
  },
  showConfirmationDialog: (message) => ipcRenderer.invoke('show-confirmation-dialog', message)
});