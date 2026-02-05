# Todo In-Memory Python Console App

A simple, command-line based todo application that stores tasks in memory using Python.

## Overview

This is a console-based todo application that allows users to manage tasks without any persistent storage. All tasks are stored in memory and will be lost when the application exits.

## Features

- Add tasks with title and description
- Delete tasks by ID
- Update task title and/or description
- View all tasks with their completion status
- Mark tasks as complete/incomplete

## Prerequisites

- Python 3.13 or higher
- For Windows users: WSL 2 with Ubuntu 22.04

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Navigate to the source directory:
   ```bash
   cd src/
   ```

## Usage

To run the application, navigate to the `src/` directory and execute:

```bash
python todo_app.py
```

The application will present you with an interactive menu:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Exit

Follow the on-screen prompts to interact with the application.

## Project Structure

```
src/
├── todo_app.py              # Main CLI application
├── models/
│   └── task.py             # Task data model and operations
└── utils/
    └── cli_helpers.py      # CLI utility functions
```

## Architecture

- **In-memory storage**: Tasks are stored in Python data structures (lists/dictionaries) during runtime
- **Modular design**: Separation of concerns between CLI interface, data models, and utilities
- **Simple validation**: Basic input validation to prevent errors

## Development

The application follows a simple architecture where:
- `models/task.py` handles all task-related operations
- `utils/cli_helpers.py` provides utility functions for CLI interaction
- `todo_app.py` orchestrates the application flow

## Testing

Manual testing can be performed by running the application and verifying all features work as expected through the interactive menu.
