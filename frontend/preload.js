const { contextBridge, ipcRenderer } = require('electron');

let settings;
let themeSettings;

ipcRenderer.on('send-settings', (event, data) => {
  settings = data;
});

ipcRenderer.on('theme-settings', (event, data) => {
  themeSettings = data;
});

contextBridge.exposeInMainWorld('api', {
  send: (channel, data) => {
    let validChannels = [
      'close-app', 
      'minimize-app', 
      'maximize-app', 
      'toggle-fullscreen', 
      'create-new-main-window', 
      'get-settings', 
      'get-theme-settings', 
      'save-settings', 
      'hard-refresh',
      'change-theme'
    ];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },
  recieve: (channel, func) => {
    let validChannels = ['reply', 'send-settings', 'theme-settings', 'theme-change'];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => func(...args));
    }
  },
  require: (module) => {
    if (module === 'electron') {
      return { ipcRenderer };
    }
  },
  getSettings: () => settings,
  getThemeSettings: () => themeSettings
});
