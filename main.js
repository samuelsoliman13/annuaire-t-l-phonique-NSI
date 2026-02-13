const { app, BrowserWindow, ipcMain, net, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const Store = require('electron-store');

const store = new Store();

let pythonProcess;
let mainWindow;
let choiceWindow;

function createChoiceWindow() {
  choiceWindow = new BrowserWindow({
    width: 400,
    height: 250, // Hauteur augmentée pour accommoder la case à cocher
    icon: path.join(__dirname, 'icon.png'), // icône pour la fenêtre de choix
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    }
  });

  choiceWindow.loadFile('choice.html');
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, 'icon.png'), // icône pour la fenêtre principale
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  });

  mainWindow.loadFile('index.html');
}

// Fonction pour attendre que le serveur soit prêt
async function waitForServer(url, maxRetries = 30) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const request = net.request(new URL('/api/health', url).toString());
      const isReady = await new Promise((resolve) => {
        const timeout = setTimeout(() => {
          request.abort();
          resolve(false);
        }, 2000);

        request.on('response', (response) => {
          clearTimeout(timeout);
          resolve(response.statusCode === 200);
        });

        request.on('error', () => {
          clearTimeout(timeout);
          resolve(false);
        });

        request.on('abort', () => {
          clearTimeout(timeout);
          resolve(false);
        });

        request.end();
      });

      if (isReady) {
        console.log(`Server is ready after ${i} retries`);
        return true;
      }
    } catch (error) {
      console.error(`Retry ${i}: ${error.message}`);
    }

    await new Promise(resolve => setTimeout(resolve, 500)); // Attendre 500ms avant le prochain essai
  }

  console.error('Server did not respond after maximum retries');
  return false;
}

// Fonction pour gérer l'initialisation de la base de données et la création de la fenêtre
async function handleDbChoice(choice) {
  console.log('Received db-choice:', JSON.stringify(choice, null, 2));
  if (choiceWindow) {
    choiceWindow.close();
    choiceWindow = null;
  }
  createWindow();

  let apiBaseUrl;

  if (choice.type === 'local') {
    // Tuer le processus Python précédent s'il existe
    if (pythonProcess) {
      console.log('Killing previous Python process');
      pythonProcess.kill();
      pythonProcess = null;
    }

    const dbUri = `sqlite:///${path.join(app.getPath('userData'), 'contacts.db')}`; // Utiliser le chemin des données de l'application pour SQLite
    
    if (app.isPackaged) {
      const apiExePath = path.join(process.resourcesPath, 'build', 'python', 'api_server.exe');
      pythonProcess = spawn(apiExePath, ['--db-uri', dbUri]);
    } else {
      pythonProcess = spawn('python', ['api_server.py', '--db-uri', dbUri]);
    }

    pythonProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });
    apiBaseUrl = 'http://127.0.0.1:5001';
    
    // Attendre que le serveur soit vraiment prêt
    const serverReady = await waitForServer(apiBaseUrl);
    if (!serverReady) {
      console.error('Failed to start local Python server');
    }
    console.log('Local Python server started with DB URI:', dbUri);
  } else {
    apiBaseUrl = choice.url;
    console.log('Using remote API URL:', apiBaseUrl);
  }
  
 //Attendre que la page soit chargée
  mainWindow.webContents.once('did-finish-load', () => {
    console.log('Main window loaded, sending db-url:', apiBaseUrl);
    mainWindow.webContents.send('db-url', apiBaseUrl);
  });

  // Sauvegarder le choix si 'remember' est vrai
  if (choice.remember) {
    store.set('dbChoice', choice);
  } else {
    store.delete('dbChoice');
  }
}

app.whenReady().then(() => {
  const rememberedChoice = store.get('dbChoice');
  if (rememberedChoice) {
    console.log('Using remembered database choice:', rememberedChoice.type);
    handleDbChoice(rememberedChoice);
  } else {
    createChoiceWindow();
  }
});

ipcMain.on('db-choice', (event, choice) => {
  handleDbChoice(choice);
});

// Gestionnaire IPC pour oublier le choix mémorisé
ipcMain.on('forget-db-choice', () => {
  store.delete('dbChoice');
  console.log('Remembered database choice cleared. Restarting app.');
  if (mainWindow) mainWindow.close();
  if (pythonProcess) pythonProcess.kill();
  app.relaunch();
  app.quit();
});

ipcMain.handle('ping-url', async (event, url) => {
  try {
    const healthUrl = new URL('/api/health', url).toString();
    return new Promise((resolve) => {
      const request = net.request(healthUrl);

      const timeout = setTimeout(() => {
        request.abort();
      }, 5000); // 5-second timeout

      request.on('response', (response) => {
        clearTimeout(timeout);
        resolve(response.statusCode === 200);
      });

      request.on('error', (error) => {
        clearTimeout(timeout);
        console.error(`Ping error: ${error.message}`);
        resolve(false);
      });

      request.on('abort', () => {
        clearTimeout(timeout);
        // The 'abort' event can be triggered by the timeout itself, so a specific log isn't always needed,
        // but it's good to resolve false in case of an external abort.
        resolve(false);
      });

      request.end();
    });
  } catch (error) {
    console.error(`Invalid URL for ping: ${url}`);
    return false; // Invalid URL
  }
});

ipcMain.handle('show-confirmation-dialog', async (event, message) => {
  const result = await dialog.showMessageBox(BrowserWindow.getFocusedWindow(), {
    type: 'question',
    buttons: ['Yes', 'No'],
    defaultId: 1, // 'No' is the default button
    title: 'Confirmation',
    message: message,
  });
  return (result.response === 0); // Returns true if 'Yes' is clicked (index 0)
});


app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    if (pythonProcess) {
      console.log('Killing Python process on app close');
      pythonProcess.kill('SIGTERM');
      // Forcer la termination après 3 secondes si le processus n'a pas fermé
      setTimeout(() => {
        if (pythonProcess) {
          pythonProcess.kill('SIGKILL');
        }
      }, 3000);
    }
    app.quit();
  }
});

app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) {
    if (!mainWindow && !choiceWindow) { // Créer uniquement la fenêtre de choix si aucune fenêtre principale n'est ouverte
      const rememberedChoice = store.get('dbChoice');
      if (rememberedChoice) {
        console.log('Using remembered database choice:', rememberedChoice.type);
        handleDbChoice(rememberedChoice);
      } else {
        createChoiceWindow();
      }
    }
  }
});
