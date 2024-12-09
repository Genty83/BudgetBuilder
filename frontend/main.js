// Modules to control application life and create native browser window
const { app, BrowserWindow, Menu } = require('electron');
const path = require('node:path');
const ipc = require('electron').ipcMain;
const fs = require('fs').promises;

let mainWindow;
let additionalWindows = [];

const menuTemplate = [
  {
    label: 'View',
    submenu: [
      {
        label: 'Toggle Full Screen',
        accelerator: process.platform === 'darwin' ? 'Ctrl+F' : 'F11',
        click() {
          const focusedWindow = BrowserWindow.getFocusedWindow();
          if (focusedWindow) {
            focusedWindow.setFullScreen(!focusedWindow.isFullScreen());
          }
        }
      },
      {
        label: 'Toggle Developer Tools',
        accelerator: process.platform === 'darwin' ? 'Alt+Command+I' : 'Ctrl+Shift+I',
        click() {
          const focusedWindow = BrowserWindow.getFocusedWindow();
          if (focusedWindow) {
            focusedWindow.webContents.toggleDevTools();
          }
        }
      },
      {
        label: 'New Window',
        accelerator: 'CmdOrCtrl+N',
        click: () => {
          createWindow();
        }
      },
      {
        label: 'Hard Refresh',
        accelerator: 'CmdOrCtrl+R',
        click() {
          const focusedWindow = BrowserWindow.getFocusedWindow();
          if (focusedWindow) {
            focusedWindow.webContents.reloadIgnoringCache();
          }
        }
      }
    ]
  }
];

const menu = Menu.buildFromTemplate(menuTemplate);
Menu.setApplicationMenu(menu);

async function loadSettings() {
  try {
    const configPath = path.join(__dirname, '../config/app_settings.json');
    const data = await fs.readFile(configPath, 'utf8');
    const settings = JSON.parse(data);
    return settings;
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function saveSettings(settings) {
  try {
    const configPath = path.join(__dirname, '../config/app_settings.json');
    await fs.writeFile(configPath, JSON.stringify(settings, null, 2));
  } catch (error) {
    console.error(error);
  }
}

// Function to load theme settings from JSON file
async function loadThemeSettings() {
  try {
    const data = await fs.readFile(path.join(__dirname, '../themes/default-dark.json'), 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Failed to load theme settings', error);
    return null;
  }
}

async function createWindow() {
  const settings = await loadSettings();
  const themeSettings = await loadThemeSettings();

  if (!settings) {
    console.error('Failed to load settings');
    return;
  }

  // Create the browser window
  const window = new BrowserWindow({
    width: settings.window.width,
    height: settings.window.height,
    minHeight: settings.window.minHeight,
    minWidth: settings.window.minWidth,
    frame: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
  });

  // and load the index.html of the app
  window.loadURL('http://localhost:8000');

  // Set Content Security Policy
  window.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self';",
          "img-src 'self' data: https:;",
          "script-src 'self' https://fonts.googleapis.com;",
          "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;",
          "font-src 'self' https://fonts.gstatic.com;"
        ].join(' ')
      }
    });
  });

  // Send settings and theme settings to the renderer process
  window.webContents.on('did-finish-load', () => {
    window.webContents.send('settings', settings);
    window.webContents.send('theme-settings', themeSettings);
  });

  window.on('closed', () => {
    if (mainWindow === window) {
      mainWindow = null;
    } else {
      additionalWindows = additionalWindows.filter(w => w !== window);
    }
  });
  return window;
}

function createNewMainWindow() {
  const newWindow = createWindow();
  additionalWindows.push(newWindow);
}

ipc.on('create-new-main-window', () => {
  createNewMainWindow();
});

ipc.on('close-app', () => {
  const focusedWindow = BrowserWindow.getFocusedWindow();
  if (focusedWindow) {
    focusedWindow.close();
  }
});

ipc.on('minimize-app', () => {
  const focusedWindow = BrowserWindow.getFocusedWindow();
  if (focusedWindow) {
    focusedWindow.minimize();
  }
});

ipc.on('maximize-app', () => {
  const focusedWindow = BrowserWindow.getFocusedWindow();
  if (focusedWindow) {
    focusedWindow.isMaximized() ? focusedWindow.unmaximize() : focusedWindow.maximize();
  }
});

ipc.on('toggle-fullscreen', () => {
  const focusedWindow = BrowserWindow.getFocusedWindow();
  if (focusedWindow) {
    focusedWindow.setFullScreen(!focusedWindow.isFullScreen());
  }
});

ipc.on('get-settings', async (event) => {
  const settings = await loadSettings();
  event.reply('send-settings', settings);
});

ipc.on('save-settings', async (event, newSettings) => {
  await saveSettings(newSettings);
});

ipc.on('hard-refresh', () => {
  const focusedWindow = BrowserWindow.getFocusedWindow();
  if (focusedWindow) {
    focusedWindow.webContents.reloadIgnoringCache();
  }
});

app.whenReady().then(() => {
  mainWindow = createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      mainWindow = createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
