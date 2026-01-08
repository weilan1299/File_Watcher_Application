# File Watcher Application

A Python-based tool for monitoring filesystem changes in real time with a graphical interface and persistent logging.

---

## 📌 Overview

Build a lightweight file monitoring app. It tracks changes within directories, provides a user-friendly GUI to visualize events, and stores activity logs for later analysis.

---

## 🚀 Features

- 📁 **Real-time Directory Monitoring**  
  Uses the `watchdog` library to detect and respond to file additions, deletions, and modifications as they occur.

- 🖼️ **Graphical User Interface (GUI)**  
  Built with **Tkinter**, offering a simple and intuitive interface for selecting directories and viewing event logs.

- 📝 **Persistent Logging to SQLite**  
  All file system events are logged to a local SQLite database for reliable storage and analysis.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Monitoring Engine | Python + `watchdog` |
| GUI | `Tkinter` |
| Database | SQLite |
| Platform | Cross-platform (Windows / macOS / Linux) |

---

## 🧠 How It Works

1. The application watches a user-selected directory using the `watchdog` event handler.
2. When the filesystem changes (add, modify, delete), the event handler captures and processes the event.
3. Events are displayed in the GUI in real time.
4. All events are stored in an SQLite database for later review or analytics.

---

## 📁 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/weilan1299/File_Watcher_Application.git
cd File_Watcher_Application
