# Portable Workspace

A smart, secure, and adaptive USB-based workspace system that allows students to recreate their personalized computing environment on different computers without carrying a heavy laptop every day.

## Overview

Students often have access to college computer labs, but each computer may have a different software environment and configuration. Setting up development tools, files, applications, extensions, browser tabs, and personal preferences repeatedly is inconvenient and time-consuming.

**Portable Workspace** addresses this problem by storing a portable representation of a user's workspace on a USB device.

When the USB is connected to another computer, the system:

1. Detects the host computer's operating system and available resources.
2. Detects available applications and tools.
3. Reads the user's workspace configuration.
4. Restores selected files and settings.
5. Recreates the user's VS Code development environment.
6. Uses portable or isolated applications where possible.
7. Works within the host computer's security and hardware restrictions.
8. Provides a temporary workspace that can eventually support saving or discarding session changes.

The goal is not to replace the host operating system, but to provide an **adaptive workspace layer** on top of it.

---

## Key Features

### Workspace Portability

Store a user's workspace configuration and selected files on a portable USB device.

### Application Detection

Detect whether required applications are available on the host system.

Supported applications can include:

- Visual Studio Code
- Git
- Python
- Node.js
- Other supported development tools

The system can determine:

- Whether an application exists
- Its executable path
- Its installed version
- Whether the application can be used in the current environment

### Workspace Restoration

Restore selected workspace files from the USB to a temporary host workspace.

The restoration system is designed to avoid modifying unrelated host files.

### VS Code Environment

Recreate the user's development environment, including:

- Settings
- Keybindings
- Snippets
- Extensions
- Projects
- Workspace configuration

Portable VS Code can be used where appropriate.

### Settings Restoration

Restore supported application configurations without unnecessarily overwriting the host user's permanent settings.

### Temporary Workspace

The architecture supports a temporary session model:

```text
USB Workspace
      ↓
Host Detection
      ↓
Temporary Session
      ↓
Workspace Restoration
      ↓
User Works
      ↓
Save / Discard
