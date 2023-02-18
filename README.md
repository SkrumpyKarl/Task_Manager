# Task Manager
The Task Manager is a Python program that tracks users, records tasks, and generates statistics. It is designed to help manage tasks for individuals or teams.

The code is written in Python 3.11 and run in Visual Studio Code.

## Access
To access the Task Manager with admin rights, use the following credentials:

- Username: admin
- Password: password

Without admin rights, users can only edit tasks that are assigned to them.

## Data Storage
The program uses a text file, user.txt and tasks.txt, to store user:password pairs and task information. These files are created automatically when the program is run for the first time. If the file already exists, the program will load the users and the tasks from the files.

Task Management
The Task Manager has the following features available to each user:

- View all tasks
- View tasks assigned to a specific user
- Add a new task
- Edit an existing user assigned task
- Generate statistics

When adding or editing a task, the following information is required:

- Task title
- Task description
- Due date (in the format YYYY-MM-DD)
- Assigned user
- Task completion status

## Statistics

The Task Manager generates statistics on the tasks, including:

- Total number of tasks
- Number of completed tasks
- Number of uncompleted tasks
- Percentage of completed tasks
- Percentage of uncompleted tasks
- Percentage of overdue tasks

The statistics are displayed in a table and can be printed to a text file.

## Usage
To run the Task Manager, run the Task_Manager.py file in a Python environment. The program will prompt for a username and password to log in. Once logged in, the user can access the features of the Task Manager.

## Dependencies
The following libraries are required to run the program:

- time
- datetime
- os.path
