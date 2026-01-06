const { app, BrowserWindow } = require("electron")
const { spawn } = require("child_process")
const path = require("path")

let backendProcess

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
  })

  win.loadFile(path.join(__dirname, "../frontend/index.html"))
}

app.whenReady().then(() => {
  backendProcess = spawn("python", ["../backend/main.py"])
  createWindow()
})

app.on("will-quit", () => {
  backendProcess.kill()
})
