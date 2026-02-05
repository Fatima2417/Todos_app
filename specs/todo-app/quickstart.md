# Quick Start Guide: Todo In-Memory Python Console App

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional, for dependency management)
- For Windows users: WSL 2 with Ubuntu 22.04

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Navigate to the source directory:
   ```bash
   cd src/
   ```

3. Ensure Python 3.13+ is installed:
   ```bash
   python --version
   ```

## Running the Application

1. From the `src/` directory, run:
   ```bash
   python todo_app.py
   ```

2. The application will display an interactive menu with the following options:
   - 1. Add Task
   - 2. Delete Task
   - 3. Update Task
   - 4. View Task List
   - 5. Mark Task Complete/Incomplete
   - 6. Exit

## Usage Examples

### Adding a Task
1. Select option 1 from the menu
2. Enter the task title when prompted
3. Optionally enter a description when prompted
4. The task will be added with an auto-generated ID

### Viewing Tasks
1. Select option 4 from the menu
2. All tasks will be displayed with their ID, title, and completion status

### Updating a Task
1. Select option 3 from the menu
2. Enter the task ID when prompted
3. Enter the new title or press Enter to keep the current title
4. Enter the new description or press Enter to keep the current description

### Deleting a Task
1. Select option 2 from the menu
2. Enter the task ID when prompted
3. Confirm deletion if prompted

### Marking Task Complete/Incomplete
1. Select option 5 from the menu
2. Enter the task ID when prompted
3. The completion status will toggle

## Troubleshooting

- **Python version**: If you encounter errors, verify that Python 3.13+ is installed
- **Module not found**: Ensure you're running the application from the correct directory
- **Permission errors**: Ensure you have read/write permissions for the project directory

## Notes

- All data is stored in memory only and will be lost when the application exits
- The application does not require any external dependencies beyond the Python standard library
- For Windows users, ensure WSL 2 is properly configured with Ubuntu 22.04 for optimal compatibility