const { app, BrowserWindow, Tray, Menu, screen } = require('electron');
const express = require('express');
const path = require('path');

let tray = null;

function createWindow() {
    const expressApp = express();
    const server = require('http').createServer(expressApp);
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    // Serve static files
    expressApp.use(express.static(path.join(__dirname)));

    const PORT = 9000;
    server.listen(PORT, () => {
        console.log(`Server running at http://localhost:${PORT}`);
    });

    const win = new BrowserWindow({
        width: 300,
        height: 735,
        frame: false, // Optional: Remove the window frame
        transparent: true, // Optional: Enable transparency
        backgroundColor: '#00000000', // Fully transparent background
        x: width - 300, // Position at the right edge of the screen
        y: 50,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
        // alwaysOnTop: true,
        // autoHideMenuBar: true
    });

    win.loadURL(`http://localhost:${PORT}/index.html`);
    win.webContents.setBackgroundThrottling(true);
    win.on('close', (event) => {
      event.preventDefault();
        win.hide(); // Hide the window
    });

    // Create the system tray icon
    const trayIconPath = path.join(__dirname, 'assets', 'tray-icon.png');
    tray = new Tray(trayIconPath);

    const contextMenu = Menu.buildFromTemplate([
        { label: 'Open', click: () => win.show() },
        { label: 'Quit', click: () => app.quit() },
    ]);
    tray.setContextMenu(contextMenu);
    tray.setToolTip('My Electron App');
    tray.on('double-click', () => win.show());

    // Double-click on the tray icon to show the window
    tray.on('double-click', () => {
        win.show(); // Show the window when the tray icon is double-clicked
    });
}

app.commandLine.appendSwitch('enable-transparent-visuals');
app.commandLine.appendSwitch('disable-gpu-vsync');

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
    
});

// MacOS activation
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
  }
});
