# 🧠 SMART TASK MANAGER

A modern, fully functional desktop task management application built with **Python** and **Tkinter**. Designed to help you organize tasks efficiently with smart filters, sorting, live search, progress tracking, and a clean, toggleable light/dark blue-themed UI.

---

## ✨ Features

- ✅ **Add, edit, and delete** tasks with full details
- 🔍 **Search** tasks in real time by title or description
- 🎯 **Filter** tasks by status (e.g., `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`)
- 🗂️ **Sort** by `deadline` or `priority`
- 📅 **Deadline highlighting**:
  - 🔴 Overdue tasks in red
  - 🟡 In-progress tasks in yellow
  - 🟢 Completed tasks in green
- 📈 **Visual progress bar** for completed tasks
- 🌓 **Light/Dark theme toggle** with modern blue UI
- 🖱️ Right-click context menu to edit/delete tasks
- 📁 Data persistence using local JSON (`tasks.json`)
- 📌 Clean, organized codebase using **OOP and MVC principles**

---

## 📂 Project Structure

```
C:.
│   main.py                 # Entry point of the app
│   README.md
│
├───core
│   │   file_handler.py     # Load/save task data from JSON
│   │   task.py             # Task class with all attributes
│   │   task_manager.py     # Logic to manage tasks (CRUD, filter, sort)
│
├───data
│   │   tasks.json          # Stores all task data (auto-created if missing)
│
└───gui
    │   main_window.py      # GUI dashboard, task list, search, sort, filter, theme
    │   task_editor.py      # GUI for adding/editing tasks
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI:** Tkinter
- **Data Storage:** JSON
- **Design:** Custom blue theme with Cambria/Times New Roman fonts

---

## 🚀 How to Run

1. **Clone the repo** or download the source files.

2. Ensure you have **Python 3.6+** installed.

3. From the root directory, run:

   ```bash
   python main.py
   ```

   That’s it! The GUI will launch, and you're good to go.

---

## 📸 Screenshots
> ![Dashboard Preview] (Screenshots/Screenshot 2025-03-11 180003.png)
> ![Dashboard Preview] (Screenshots/Screenshot 2025-03-11 180408.png)
> ![Task Description] (Screenshots/Screenshot 2025-03-11 180414.png)
> ![Right Click Facility] (Screenshots/Screenshot 2025-03-11 180425.png)
> ![Light Mode] (Screenshots/Screenshot 2025-03-11 180503.png)


---

## 🧩 Future Improvements (Ideas)

- 🔔 Task notifications/reminders
- 📤 Export tasks to CSV or Excel
- 📆 Calendar view for upcoming deadlines
- 🌐 Web version using Flask or Django

---

## 🧑‍💻 Author

**Shivraj Anand**  
Open to freelance, research collaboration, and remote internships.  
Let’s connect!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
