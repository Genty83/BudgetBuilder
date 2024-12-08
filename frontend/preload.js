const { contextBridge, ipcRenderer } = require('electron');

let settings;

ipcRenderer.on('send-settings', (event, data) => {
  settings = data;
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
      'save-settings', 
      'hard-refresh'
    ];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },
  recieve: (channel, func) => {
    let validChannels = ['reply', 'send-settings'];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => func(...args));
    }
  },
  require: (module) => {
    if (module === 'electron') {
      return { ipcRenderer };
    }
  },
  getSettings: () => settings
});
