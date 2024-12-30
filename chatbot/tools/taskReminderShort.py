class TaskReminder:
    def __init__(self, filename):
        self.filename = filename | "tasklist.txt"
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create the file
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            for task in self.tasks:
                f.write(task + '\n')

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, task_number):
        try:
            del self.tasks[task_number - 1]
            self.save_tasks()
        except IndexError:
            print("Invalid task number.")

    def clear_tasks(self):
        self.tasks = []
        self.save_tasks()

    def get_tasks(self):
        if self.tasks:
            task_list = "Task List:\n" + "\n".join(["- " + task for task in self.tasks])
            return task_list
        else:
            return "No tasks for now, Master."


# # # Example usage:
# reminder = TaskReminder('tasks.txt')

# while True:
#     print("\nOptions:")
#     print("1. Add task")
#     print("2. Delete task")
#     print("3. Clear tasks")
#     print("4. List tasks")
#     print("5. Exit")

#     option = input("Choose an option: ")

#     if option == '1':
#         task = input("Enter a task: ")
#         reminder.add_task(task)
#     elif option == '2':
#         task_number = int(input("Enter the task number to delete: "))
#         reminder.delete_task(task_number)
#     elif option == '3':
#         reminder.clear_tasks()
#     elif option == '4':
#         print(reminder.get_tasks())
#     elif option == '5':
#         break
#     else:
#         print("Invalid option. Please choose again.")