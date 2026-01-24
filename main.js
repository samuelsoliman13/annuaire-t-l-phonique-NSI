const { app, BrowserWindow, ipcMain } = require('electron');
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
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  });

  mainWindow.loadFile('index.html');
}

// Fonction pour gérer l'initialisation de la base de données et la création de la fenêtre
async function handleDbChoice(choice) {
  if (choiceWindow) {
    choiceWindow.close();
    choiceWindow = null;
  }
  createWindow();

  let apiBaseUrl;

  if (choice.type === 'local') {
    const dbUri = `sqlite:///${path.join(app.getPath('userData'), 'contacts.db')}`; // Utiliser le chemin des données de l'application pour SQLite
    // Spawn the Python process with the db-uri argument
    pythonProcess = spawn('python', ['api.py', '--db-uri', dbUri]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });
    apiBaseUrl = 'http://localhost:5000';
    // Give the Python server a moment to start up
    await new Promise(resolve => setTimeout(resolve, 3000)); 
    console.log('Local Python server started with DB URI:', dbUri);
  } else {
    // For remote, the API URL is provided directly, no Python process spawned here
    apiBaseUrl = choice.url;
    console.log('Using remote API URL:', apiBaseUrl);
  }

  // Send the API base URL to the renderer process
  mainWindow.webContents.send('db-url', apiBaseUrl);

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


app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    if (pythonProcess) {
      pythonProcess.kill();
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
