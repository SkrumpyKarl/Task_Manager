# ********************************TASKS'R'US***********************************
""" This Task Manager will track users, record tasks and generate statistics.

Note - use the following username and password to access with 'admin rights'.
# username: admin
# password: password

Admin can view and edit all tasks regardless of 'assigned user', otherwise
tasks can only be edited by their 'assigned user'.

See README for further information. 

"""
# Import functions
import time
from datetime import datetime, date
from os.path import exists

# Associated Files - If modified, new files readily created.
userfile = "user.txt"
taskfile = "tasks.txt"
user_overview = "user_overview.txt"
task_overview = "task_overview.txt"

# Defined Functions

def file_exists(filename):
    """
    Function to check if file exists in folder.
    """
    # If file does not exist, return false.
    file_exists = exists(filename)
    
    return file_exists


def task_dict_checker(task_dict):
    """
    Function top check if copied file lines is empty.
    """
    # If dictionary empty, returns false.
    task_dict_check = bool(task_dict)
        
    return task_dict_check 


def line_divider():
    """
    Function to print solid unicode line in terminal.
    """
    print("")
    print('\u2501' * 79)
    print("")


def read_user(userfile):
    """
    Function to read admin:password and return key:value dict pairs.
    """
    # Check userfile existings, else create new blank file with admin rights.
    file_checker = file_exists(userfile)
    if file_checker == False:    
        with open(userfile,"w") as file:
            file.write("admin;password")    
    # Take username.txt, format for dictionary construction whilst in loop.
    user_password_dict = {}
    with open(userfile,"r") as file:
            for lines in file:
                temp = lines.strip()
                # Multiple assignment.
                usernames, passwords = temp.split(";")
                user_password_dict[usernames] = passwords

    return user_password_dict


def user_login(user_password_dict):
    """
    Function to log-in user, return log status and user_name
    """
    # Define count for log-in attempts.
    count = 0
    logged_in = False
    # Log-in Attempt loop structue.
    while not logged_in:
        # 3 Log-in attempts allowed for.
        if count < 3:
            user_name = input("Please enter your username : ").lower()
            pass_word = input("Please enter your password : ")
            # Log-in True when key:value in user_pass_dict match.
            if user_name in user_password_dict.keys() and\
            pass_word == user_password_dict[user_name]:
                line_divider()
                print(f"Welcome User : {user_name}.")
                logged_in = True
            # Log-in fails when either user or pass incorrect.
            elif user_name not in user_password_dict.keys() or \
            pass_word != user_password_dict[user_name]:
                print("\nOne of your data entries is incorrect,"\
                      " please try again.")
                # Add to count on each attempt.
                count += 1
                print(f"\nAttempt {count} of 3No.\n") 
                # If log-in attempts exceed 3, make user wait.
                if count >=3:
                    print("\nYou have timed out. Wait 10 seconds\n")
                    time.sleep(10)
                    # Reset count, restart.
                    count = 0
                continue
    line_divider()

    return logged_in, user_name


def task_compiler(taskfile):
    """
    Function to construct tasks from file into dictionary containing
    number keys : task values
    """
    # Check if task file exists, else create new blank file for given name.
    if not file_exists(taskfile):
        open(taskfile, "w").close()

    # Create list of tasks from file.
    with open(taskfile, "r") as file:
        tasks = [line.strip().split(";") for line in file]

    # Construct dictionary with task number keys.
    task_dict = {i+1: task for i, task in enumerate(tasks)}

    return task_dict


def reg_user(user_password_dict,userfile):
    """
    Function to register new users, all users can currently add new users.
    """
    # Banned Usernames
    banned_usernames = ["e"]
    # Loop logic for adding new user.
    while True:
        # User names not case sensitive.
        new_user_name = input("Please enter the new username"\
                              " or 'e' to return to menu : ").lower()
        # Existing username check. 
        if new_user_name in user_password_dict.keys():
            print("\nThis username is unavailable, try a different name.\n")
            continue 
        # check for exit word and other banned_usernames.
        elif new_user_name in banned_usernames:
            break
        new_pass_word = input("Plese enter the new password : ")
        
        # Add new user:password pair to user_password_dict. 
        with open(userfile,"a") as file:
            file.write(f"\n{new_user_name};{new_pass_word}")
            print("\nNew User added")
            break
    user_password_dict = read_user(userfile)
    
    return user_password_dict


def valid_date():
    """
    Function to format user date and check if real calander date.
    """
    is_date_valid = True
    while is_date_valid:
        try:
            input_date = input("(DD/MM/YYYY) : ")
            # Multiple Assignement for formatting.
            day, month, year = input_date.split("/")
            # Check year is 4 characters long. 
            if len(year) != 4:
                    raise ValueError
        # Value Error on user not using "/" for split.
        except ValueError:
            print("\nInput date is not valid, try again.\n")
            continue
        try:
            datetime(int(year), int(month),int(day))
        # Value Error on user not using real date.
        except ValueError:
            print("Input date is not valid, try again")
            continue
        # User input formatted for single case, preps for datetime convsersion.
        input_date = f"{year}-{month}-{day}"
        break

    return input_date


def add_task(user_password_dict, taskfile,task_dict):
    """
    Function to add new task to task file name.
    """
    task_dict_check = task_dict_checker(task_dict)
        # Task creation loop.
    while True:
        assigned_user = input("Enter the task's assigned user"\
                              " or 'e' to return to menu : ").lower() 
        # Checks if assigned user is registered, else prompts another name.
        # If user input not in dictionary, print error, restart.
        if assigned_user not in user_password_dict.keys():
            if assigned_user == "e":
                break
            else:
                print("\nThis user does not exist, try again")
                line_divider()   
            continue

    # User to input task descriptors.
        task_title = input("Enter task title : ")
        task_desc = input("Enter the task description : ")    
        start_date = date.today()    
        print("Due Date ",  end= "")    
    # Calls valid_Date function, checks format and if real.
        due_date = valid_date()                
    # Automatically 'Open' on creation.
        status = "Open"   
    # As 'Open', no completion date. (Future functionality TBC).
        completed_date = "Not closed"   
    # Appends task to existing task file as string in specific order.
        with open(taskfile, "a") as file:
        # If task file is empty, write to line. 
            if task_dict_check == False:
                file.write(f"{task_title};"\
                           f"{assigned_user};"\
                           f"{start_date};"\
                           f"{due_date};"\
                           f"{status};"\
                           f"{completed_date};"\
                           f"{task_desc}")
            # Print check on writing completion.
                print("\nNew task assigned")   
        # If task file populated, write line with new '\n'.
            else:
                file.write(f"\n{task_title};"\
                           f"{assigned_user};"\
                           f"{start_date};"\
                           f"{due_date};"\
                           f"{status};"\
                           f"{completed_date};"\
                           f"{task_desc}")
                print("\nNew task assigned")
        break


def task_window(task_dict,task_filter,user_name):
    """
    Function to call compuiled task dict, extract data and present as menu 
    to user.
    """
    # Check if task dict is empty, return to menu if empty.
    task_dict_check = task_dict_checker(task_dict)
    if task_dict_check == False:
        print("There are no assigned tasks yet,"\
              " please add tasks in Menu Options.")
        line_divider()
    # When user_menu task_filter is False, all tasks called from task dict.
    elif task_filter == False:
        for key, value in task_dict.items():
            task_window_menu(key,value)   
    # When user_menu task_filter is True, only user tasks called.
    elif task_filter == True:
        for key, value in task_dict.items():
            if value[1] == user_name: 
                task_window_menu(key,value)

    return task_dict_check


def task_window_menu(key,value):
    """
    Function to present any value from task_dict, calls nested items.
    """
    print("TASK READOUT\n")
    print("Task I.D. \t\t: ", end ="")
    print(key)
    print("Task Title \t\t: ", end= "")
    print(value[0])
    print("User Assigned \t\t: ", end= "")
    print(value[1])
    print("Date Assigned \t\t: ", end= "")
    print(value[2])
    print("Due Date \t\t: ", end= "")
    print(value[3])
    print("Task Status \t\t: ", end= "")
    print(value[4])
    print("Date Completed \t\t: ", end= "")
    print(value[5]) 
    print("Task Description \t: ", end= "")
    print(f"\n\n{value[6]}")
    line_divider()


def task_editor_menu(taskfile, task_dict, user_name):
    """
    Function to display a task editor menu and prompt the user for a menu code.
    Returns the selected menu code.
    """
    print("Task Editor Menu Option Codes\n")
    # To underline menu headings.
    print("\x1B[4mCodes\x1B[0m\t \x1B[4mOptions\x1B[0m")
    # To create solid boarder between menu code and description.
    print("""             
1 \t\b\b\b\u2502\t Select Task by Task I.D.,
e \t\b\b\b\u2502\t Exit Task Editor,
    """)

    # Prompt user for menu code.
    while True:
        user_option = input("Please enter Task Editor Menu Code : ").lower()

        if user_option == "1":
            # Try/Except for selecting valid Task I.D. key.
            try:
                task_to_edit = int(input("Enter Task I.D. to edit : "))
                line_divider()
            # If not integer, return value error message to user.
            except ValueError:
                line_divider()
                print("Not a valid Task I.D. number.")
                line_divider()
                continue

            # Call dict key to get value, if key does not exist return message.
            task_value_list = task_dict.get(task_to_edit, "Task Not Found.")
            if task_value_list == "Task Not Found.":
                print("Task I.D. does not exist.")
                line_divider()
                continue
            # Check logged in user has rights to edit specific tasks.
            # Admin has rights to edit any task (user must know I.D. from 'va')
            elif user_name != "admin" and task_value_list[1] != user_name:
                print("You can only make changes to your assigned tasks.")
                line_divider()
                continue
            else:
                # Call task editor menu, returns modified value list.
                task_value_list = task_editor(task_to_edit, task_value_list)
                # Updates specified dict key with modified value list.
                task_dict[task_to_edit] = task_value_list
                # Call write tasks update function, writes modified to file.
                write_tasks_update(taskfile, task_dict)
                return user_option

        elif user_option == "e":
            return user_option

        else:
            print("Not a valid menu option, try again.")


def task_editor(task_to_edit, task_value_list):
    """
    Function to  display sub-menu of task editor, changing task elements.
    """
   # Sub-menu loop.
    while True:
        
        print(f"Task I.D. {task_to_edit} - Task Editor Sub-Menu Options : \n")
        # Unicode to underline menu headings.
        print("\x1B[4mCodes\x1B[0m\t \x1B[4mOptions\x1B[0m")
        # Formatting and unicode to setup menu boarders.
        print("""
1 \t\b\b\b\u2502\t Mark the task as Open/Closed,
2 \t\b\b\b\u2502\t Assigned User,
3 \t\b\b\b\u2502\t Edit Task Title,
4 \t\b\b\b\u2502\t Edit Task Description,
5 \t\b\b\b\u2502\t Edit Due Date
e \t\b\b\b\u2502\t Exit Task Sub-Menu Editor,
""")
        user_option3 = input("Please enter Task Editor"\
                             " Sub-Menu Code : ").lower() 
        line_divider()

        # Value indexing calls relevant elements for editing. Standard format.
        # Option 1 - Edit Task Status Open/Closed binary selection.
        if user_option3 == "1":
            task_value_list[4] = input(f"Task I.D. {task_to_edit} -"\
                                        " Change Status"\
                                        " (Open/Closed) : ").capitalize()
            # If user inputs closed, change to closed and closed date.
            if task_value_list[4] == "Closed":
                task_value_list[5] = date.today()
                print("Change Completed.")
                line_divider()
                continue
            # If user inputs open, reopen and remove closed date.
            elif task_value_list[4] == "Open":
                task_value_list[5] = "Not Closed"
                # Check Message.
                print("Change Completed.")
                line_divider()
                continue
            # Handle invalid data entry. Return to sub-menu. 
            else:
                print("Not valid data field entry, try agian.")
                line_divider()
        # If Task is Open, permit edits to desciptors. 
        if task_value_list[4] == "Open":
        # Option 2 - Assigned User
            if user_option3 == "2":
                new_assigned_user = input("Enter new assigned user  : ")
                if new_assigned_user in user_password_dict.keys():
                    task_value_list[1] = new_assigned_user
                    print("Change Completed.")
                    line_divider()
                else: 
                    print("\nThis user does not exist, try a different name.")
                    line_divider()
                    continue
            # Option 3 - Edit Task Title.
            elif user_option3 == "3":
                task_value_list[0] = input(f"Task I.D. {task_to_edit} -"\
                                            " Change Task"\
                                            " Title : ").capitalize()
                # Confirmation.
                print("Change Completed.")
                line_divider()
            # Option 4 - Edit Task Description.
            elif user_option3 == "4":
                task_value_list[6] = input(f"Task I.D. {task_to_edit} -"\
                                            " Change Task"\
                                            " Description : ").capitalize()
                # Confirmation.
                print("Change Completed.")
                line_divider()
            # Option 5 - Edit Due Date
            elif user_option3 == "5":
                print(f"Task I.D. {task_to_edit} - Change Due Date", end=" ")
                # Calls valid_date function.
                task_value_list[3] = valid_date()
                # Confirmation.
                print("Change Completed.")
                line_divider()    
            elif user_option3 == "e":
                break
            else:
                # Handle invalid sub-menu inputs.
                print("Not a valid menu option, try again.")
                         
        # If task is closed, task unable to be edited without reopening. 
        else: 
            print("This task is closed and unable to be edited.")
            line_divider()
            break
        
    return task_value_list


def write_tasks_update(taskfile,task_dict):
    """
    Function to write updated task value lists as string to taskfile.
    """
    # Empty string value for population.
    task_dict_file_strs = ""
    # For Loop, create f-strings for each modified items.
    for value in task_dict.values():
        task_dict_file_strs += (f"{value[0]};{value[1]};{value[2]};"
                                f"{value[3]};{value[4]};{value[5]};"
                                f"{value[6]}\n")


    # Write file strings to taskfile.
    with open(taskfile,"w") as file:
        file.write(task_dict_file_strs)


def write_statistics(task_overview,
                     total_stats_list, 
                     user_overview, 
                     all_user_stats_dict):
    """
    Function to write ordered statistics (all tasks + users) to relevant files.
    """
    # Write to taskoverview file, total stats list as str in window function.
    with open(task_overview, "w") as file:
        file.write(statistics_overview_window(total_stats_list))
        file.write("\nStatistic Code :\n")
        file.write(str(total_stats_list))

    # Write to userovervierw file, total stats as str in window function.
    with open(user_overview,"w") as file:    
        file.write(user_overview_window(all_user_stats_dict))
        file.write("Statistic :\n")
        file.write(str(all_user_stats_dict))

    # Check print.
    print("Reports generated successfully.")


def statistics_overview_window(total_stats_list):
    """
    Function to present stats from total statistics list, call nested items 
    for user to view.
    """
    lines = f"All Recorded Task Statistics\n\n"\
            f"Total Number of Recorded Tasks   : {total_stats_list[0]} No.\n"\
            f"Total Number of Closed Tasks     : {total_stats_list[1]} No.\n"\
            f"Total Number of Open Tasks       : {total_stats_list[2]} No.\n"\
            f"Total Number of Overdue Tasks    : {total_stats_list[3]} No.\n"\
            f"Percentage of Open Tasks         : {total_stats_list[4][0]}\n"\
            f"Percentage of Open Tasks Overdue : {total_stats_list[4][1]}\n"

    return lines


def user_overview_window(all_user_stats_dict):
    """
    Function to present statistics from all user statistics lists, 
    call nested items for user to view.
    """   
    # lines variable to populate.
    lines = ""
    # For loop to call each user's stats values to line...
    for key,value in all_user_stats_dict.items():
        line = f"Recorded Task Statistics for User : {key}\n\n"\
               f"Total Number of Recorded Tasks   : {value[0]} No.\n"\
               f"Total Number of Closed Tasks     : {value[1]} No.\n"\
               f"Total Number of Open Tasks       : {value[2]} No.\n"\
               f"Total Number of Overdue Tasks    : {value[3]} No.\n"\
               f"Percentage of Open Tasks         : {value[4][0]}\n"\
               f"Percentage of Open Tasks Overdue : {value[4][1]}\n\n"
        # ...Conjugate each line to lines.
        lines = lines + line

    return lines


def date_checker(date1, date2):
    """
    Function to check and compare datetime objects, returning bool object
    for validation.
    """
    # Define Datetime legal format. 
    date_format = "%Y-%m-%d"
    # When called, check if today (date 1) is after due date (date 2).
    date2 = datetime.strptime(date2,date_format)
    # Bool output True/False.
    date_check = date1 > date2
       
    return date_check


def statistics_codes(task_dict, user_password_dict):
    """ 
    Function to generate report statistics codes as nested lists
    for all users from task dictionary. 
    
    Format to store count data per iterable task in order: 
    1) task count,
    2) closed count, 
    3) open count, 
    4) open & overdue count.
    """
    # All Tasks - Generate Task Overview Stats List
    total_stats_list = [0,0,0,0]
    for task in task_dict.values():
        # Call task_stat counter function.
        count_list = task_stat_counter(task)
        # For each key value, use list comprehension for total count assignment
        total_stats_list = [total_stats_list[i] + count_list[i]\
                            for i in range(len(count_list))]

    # Call task percentage functio using full counts list.
    temp_stats = task_percent(total_stats_list[2],
                              total_stats_list[0],
                              total_stats_list[3])
    # Cast task percentage list class.
    total_percent_list = list(temp_stats)
    # Append tas kpercentages  to total_stats_list.
    total_stats_list.append(total_percent_list)
        
    # All User Tasks - Generate User Overview Stats Lists
    all_user_stats_dict = {}
    # cycle through each username in user password dictionary.
    for user in user_password_dict.keys():
        temp_stats_list = [0,0,0,0]
        # Nested for loop to iterate values per key.
        for task in task_dict.values():
            # Filter for tasks assigned to ordered dictionary keys.
            if task[1] == user:
                # Call task_stat counter function.
                count_list = task_stat_counter(task)
                # List comprehension for addition assignment.
                temp_stats_list = [temp_stats_list[i]+ count_list[i]\
                                   for i in range(len(count_list))]
        # Call user overview percentage from shared function.       
        temp_stats = task_percent(temp_stats_list[2],
                                  temp_stats_list[0],
                                  temp_stats_list[3])
        # Assign user overview percentage returns as own list then nest.
        temp_percent_list = list(temp_stats)  
        temp_stats_list.append(temp_percent_list)
        # Final user_stats_dict for user overview file. 
        all_user_stats_dict[user] = temp_stats_list 
        
    return total_stats_list, all_user_stats_dict


def task_stat_counter(value):
    """
    Function to count each task_dict value code.
    """
    # Empty Stats Counters.
    task_count = 0
    closed_count = 0
    open_count = 0
    open_overdue_count = 0

    # For each item, count given conditions below.
    task_count += 1    
    if value[4] == "Closed":
        closed_count += 1
    if value[4] == "Open":
        open_count += 1
    if value[4] == "Open":   
        date_check = date_checker(datetime.today(), value[3])
        if date_check == True:        
            open_overdue_count += 1

    # Return values can be assigned to either task overview or user overview.
    return task_count,closed_count,open_count,open_overdue_count,


def task_percent(open_count, task_count, open_overdue_count):
    """
    Function to calculate percentages given populated stats counters.
    Round to 2 d.p.
    """
    if open_count == 0:
        percent_incomplete = "All Tasks Closed."
    elif task_count == 0:
        percent_incomplete = "There are no assigned tasks yet."
    else:
        percent_incomplete = f"{round((open_count / task_count * 100),2)}%"
        
    if open_overdue_count == 0:
        percent_overdue = "No overdue user tasks."
    elif open_count == 0:
        percent_overdue = "No open user tasks."
    else:
        percent_overdue = f"{round((open_overdue_count / open_count * 100),2)}%"
       
    return percent_incomplete, percent_overdue 


def read_last_line (filename):
    """
    Function to read last line inside a given task txt file.
    Used to read string codes from an existing text file.
    """
    with open(filename,"r") as file:
        for line in file.readlines() [-1:]:
            last_line = line

    return last_line


def log_off(logged_in):
    """
    Function to change logged-in status of user.
    """
    logged_in = False

    return logged_in


def user_menu(logged_in):
    """
    Function to display user main navigiation menu.
    """
    # Only accessible when log status == True.
    if logged_in:
        
        # Check determining whether a change has been made by the user.
        task_editor_check = False
        
        while logged_in:
            print("Task Manger Menu Option Codes : \n")
            # Unicode to underline menu headings.
            print("\x1B[4mCodes\x1B[0m\t \x1B[4mOptions\x1B[0m")
            # Unicode and formatting to display menu keys and descriptions.
            print("""             
1 \t\b\b\b\u2502\t Register new user,
2 \t\b\b\b\u2502\t Add new task,
3 \t\b\b\b\u2502\t View all tasks,
4 \t\b\b\b\u2502\t View my tasks & task editor,
5 \t\b\b\b\u2502\t Generate reports,
6 \t\b\b\b\u2502\t Display statistics,
7 \t\b\b\b\u2502\t Log out,
e \t\b\b\b\u2502\t Exit program
    """)
            # Per loop, call these functions to refresh for changes made.
            user_password_dict = read_user(userfile)
            task_dict = task_compiler(taskfile)
                                    
            user_option = input("Please Enter Menu Option Code : ").lower()
            line_divider()         
            
            # Option 1 - Register a new user.            
            if user_option == "1":
                user_password_dict = reg_user(user_password_dict,userfile)
                line_divider()
                
            # Option 2 - Add new tasks. 
            elif user_option == "2":
                add_task(user_password_dict,taskfile,task_dict)
                line_divider()
                
            # Option 3 - View all tasks in taskfile.
            elif user_option == "3":
                 # When False - All tasks in file displayed.
                task_filter = False
                while True:
                    task_dict_check = task_window(task_dict,task_filter,
                                                  user_name)                   
                    if task_dict_check == False:
                        break
                    break
                
            # Option 4 - View my tasks & task editor access.
            elif user_option == "4":
                # When True - Only tasks matching username in file displayed.
                task_filter = True
                while True: 
                    task_dict_check = task_window(task_dict,task_filter,user_name)
                    if task_dict_check == False:                       
                        break
                    else:
                        task_editor_check = task_editor_menu(taskfile,task_dict,
                                                             user_name)
                        line_divider()
                        break
                    
            # Option 5 - Generate statistic reports.
            elif user_option == "5":
                
                # Check task_dict not empty, avoid division by zero on percent
                while True:
                    task_dict_check = task_dict_checker(task_dict)
                    if task_dict_check == False:
                        print("There are no assigned tasks yet,"\
                              " please add tasks in Menu Options.")
                        line_divider()
                        break 
                
                    # Call Statistics Code func to generate statistic codes.
                    total_stats_list, all_user_stats_dict = statistics_codes(
                        task_dict,
                        user_password_dict)
                    # Writes user friendly statistics and Statistics Codes.
                    write_statistics(task_overview,
                                     total_stats_list,
                                     user_overview,
                                     all_user_stats_dict)
                    line_divider()
                    break
                
            # Option 6 - Display Statistics (FROM FILE)
            elif user_option == "6":
                
                while True:
                    # Check task_dict not empty
                    task_dict_check = task_dict_checker(task_dict)
                    if task_dict_check == False:
                        print("There are no assigned tasks yet,"\
                              " please add tasks in Menu Options.")
                        line_divider()
                        break 
                
                    # Check user and task overview files exists.
                    file_exists_user = exists(user_overview)
                    file_exists_tasks = exists(task_overview)
                
                    # Generate statistic reports (AS OPTION 5)
                    if (file_exists_user == False or 
                        file_exists_tasks == False or
                        task_editor_check == True):
                        total_stats_list, all_user_stats_dict =\
                        statistics_codes(task_dict,user_password_dict)
                        write_statistics(task_overview,
                                         total_stats_list,
                                         user_overview, 
                                         all_user_stats_dict)
                        # Reset task editor check.
                        task_editor_check = False
                
                    # Read string statistics code, evaluate for list object.
                    last_line = read_last_line(task_overview)
                    read_total_stats_list = eval(last_line)
                
                    # Read string staticstics code, evaluate for dict object.
                    last_line = read_last_line(user_overview)
                    read_all_user_stats_dict = eval(last_line)
                
                    # Call statistics terminal window functions, print. 
                    lines = statistics_overview_window(read_total_stats_list)
                    print(lines)
                    lines = user_overview_window(read_all_user_stats_dict)
                    print(lines)
                    line_divider()
                    break
            
            # Option 7 - Log user off.
            elif user_option == "7":
                logged_in = log_off(logged_in)
            
            # Option 8 - Exit programme. Break Driver Code.
            elif user_option == "e":
                print("Have a productive day!\n")
                quit()
            else:
                # Handle invalid menu inputs.
                print("Not a valid menu option, try again.")
                line_divider()
                continue    
    
    return user_password_dict

# ********************************DRIVER CODE**********************************
print("\nWelcome to Team Task Manager.")
line_divider()
    # Call read_userfile.
user_password_dict = read_user(userfile)
    # For loop, check user credientials, user menu and log-off.
while True:     
    # Call user_login function, return log status and user_name entered.
    logged_in, user_name = user_login(user_password_dict)
    # Call user_menu function if logged in.
    user_password_dict = user_menu(logged_in)
    # When logged out, return to user_login function. 
    continue