const { contextBridge, ipcRenderer } = require('electron');

let resolveDbUrl;
const dbUrlPromise = new Promise(resolve => {
  resolveDbUrl = resolve;
});

ipcRenderer.on('db-url', (event, url) => {
  console.log('Preload received db-url:', url);
  resolveDbUrl(url); // Resolve the promise when the URL is received
});

contextBridge.exposeInMainWorld('api', {
  getDbUrl: () => dbUrlPromise, // Return the promise for consumers who need it
  fetch: async (url, options) => { // Make fetch async
    const actualDbUrl = await dbUrlPromise; // Wait for the dbUrl to be set
    if (!actualDbUrl) {
      console.error('Database URL not set!');
      return Promise.reject(new Error('Database URL not set'));
    }
    const fullUrl = `${actualDbUrl}${url}`;
    console.log(`Fetching from: ${fullUrl}`);
    try {
      const res = await fetch(fullUrl, options);
      const data = await res.json();
      if (!res.ok) {
        console.error(`HTTP Error: ${res.status} ${res.statusText}`, data);
        const errorMsg = data.erreur || `HTTP ${res.status}: ${res.statusText}`;
        throw new Error(errorMsg);
      }
      return data;
    } catch (err) {
      console.error(`Fetch error: ${err.message}`);
      throw err;
    }
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