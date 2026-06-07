# noSleep

A lightweight, zero-dependency, console-based Windows utility to prevent your computer from going to sleep or locking. 

Written in pure Python, `noSleep` is designed to be completely unobtrusive, consuming minimal resources while keeping your system awake and your status active.

---

## Features

- **No PIP Requirements**: Runs using native Windows APIs via standard Python libraries (`ctypes` and `msvcrt`). No third-party package installations are needed.
- **Visual Micro-Movements**: Every 5 minutes, it performs a 2-pixel relative hardware-simulated nudge (right and then back left), keeping cursors, screens, and chat clients active without interrupting your work.
- **Hardware-Level Emulation**: Simulates genuine hardware interrupts using `mouse_event` to ensure Windows registers activity.
- **Developer-Grade Sleep Prevention**: Calls the official Win32 API `SetThreadExecutionState` to explicitly block system idle states and display shutdowns.
- **Keyboard Shutdown**: Press `ESC` inside the console window at any time to exit cleanly and instantly restore default Windows sleep settings.
- **CLI Friendly**: Wraps execution so you can run it from any terminal window just by typing `nosleep`.

---

## Installation & Setup

### Option 1: Quick Remote One-Liner (Recommended)

You can install `noSleep` instantly without cloning the repository. Open a PowerShell terminal and run:

```powershell
irm https://raw.githubusercontent.com/tiktok-rick/noSleep/main/install.ps1 | iex
```

### Option 2: Local Installation (Cloned Repository)

If you have cloned this repository locally, run the installer script from the root folder:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

### What the installer does:
1. Creates a dedicated `.nosleep` folder in your User Profile directory (`C:\Users\<Username>\.nosleep`).
2. Copies `nosleep.py` and `nosleep.bat` to this folder.
3. Automatically appends this folder to your User `PATH` environment variable.

*Tip: After installing, you must open a **new** terminal window for the `PATH` changes to take effect.*

---

## Usage

Once installed, open a new Command Prompt or PowerShell window and type:

```cmd
nosleep
```

### Test Mode
To verify that everything is working instantly without waiting 5 minutes, run:

```cmd
nosleep --test
```
In test mode, the script nudges the cursor and logs coordinates every **5 seconds** instead of 5 minutes.

### Exiting
To exit the loop and return your Windows sleep settings to normal, simply focus the terminal window and press the **`ESC`** key (or press `Ctrl+C`).

---

## Uninstallation

If you wish to remove the tool:

1. Open PowerShell and remove the files and directory:
   ```powershell
   Remove-Item -Recurse -Force "$HOME\.nosleep"
   ```
2. Remove the folder from your User `PATH` via Environment Variables or PowerShell:
   ```powershell
   $path = [Environment]::GetEnvironmentVariable("PATH", "User") -split ";"
   $newPath = ($path | Where-Object { $_ -ne (Join-Path $HOME ".nosleep") }) -join ";"
   [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
   ```

---

## How It Works

Windows ignores simple software cursor adjustments (like `SetCursorPos`) when calculating idle timeouts. `noSleep` overcomes this using two distinct mechanisms:

1. **`SetThreadExecutionState`**:
   Tells the Windows power manager that the running thread requires the system and display to remain active.
   ```python
   ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
   ```
2. **`mouse_event`**:
   Injects relative motion coordinates directly into the hardware input stream. Windows handles these inputs identically to physical mouse movement, resetting the system-wide idle timer.
   ```python
   ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)
   ```

---

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This readme is partially written using AI. Use this repo at your own risk. 😊