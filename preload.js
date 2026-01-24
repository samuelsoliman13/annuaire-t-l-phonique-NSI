const { contextBridge, ipcRenderer } = require('electron');

let dbUrl;

ipcRenderer.on('db-url', (event, url) => {
  dbUrl = url;
});

contextBridge.exposeInMainWorld('api', {
  getDbUrl: () => dbUrl,
  fetch: (url, options) => {
    if (!dbUrl) {
      return Promise.reject('Database URL not set');
    }
    return fetch(`${dbUrl}${url}`, options).then(res => res.json());
  },
  on: (channel, callback) => {
    ipcRenderer.on(channel, callback);
  },
  forgetDbChoice: () => {
    ipcRenderer.send('forget-db-choice');
  }
});

contextBridge.exposeInMainWorld('ipc', {
  send: (channel, data) => {
    ipcRenderer.send(channel, data);
  }
});
