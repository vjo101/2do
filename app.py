from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
import sqlite3
from db import init_db, DB_PATH

class TodoApp(App):
    CSS_PATH = "styles.css"
    BINDINGS = [
        ("j", "down", "Move Down"),
        ("k", "up", "Move Up"),
        ("i", "focus_insert", "focus add"),
        ("escape", "unfocus_insert", "unfocus add"),
        ("enter", "add", "Add Todo"),
        (":+q", "quit", "Quit"),
    ]

    def on_mount(self):
        init_db()
        self.selected_index = 0  # Track selected todo
        self.refresh_todos()
        self.set_focus(self.query_one("#input", Input))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Todo List", id="title")
        yield Input(placeholder="Add a new todo...", id="input")
        yield Button("Add", id="add_btn")
        yield Static("", id="todos")
        yield Footer()

    def refresh_todos(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, task, done FROM todos")
        todos = c.fetchall()
        conn.close()
        todos_widget = self.query_one("#todos", Static)
        lines = []
        for idx, (_, task, done) in enumerate(todos):
            prefix = "-> " if idx == getattr(self, "selected_index", 0) else "   "
            status = "[x]" if done else "[ ]"
            lines.append(f"{prefix}{status} {task}")
        todos_widget.update("\n".join(lines))
        self.todos = todos  # Store for navigation

    def action_down(self):
        if not hasattr(self, "todos") or not self.todos:
            return
        self.selected_index = min(self.selected_index + 1, len(self.todos) - 1)
        self.refresh_todos()

    def action_up(self):
        if not hasattr(self, "todos") or not self.todos:
            return
        self.selected_index = max(self.selected_index - 1, 0)
        self.refresh_todos()

    def action_focus_insert(self):
        self.set_focus(self.query_one("#input", Input))

    def action_unfocus_insert(self):
        self.set_focus(None)

    def action_add(self):
        if self.focused is self.query_one("#input", Input):
            self.on_button_pressed(self.query_one("#add_btn", Button))

    def action_quit(self):
        self.exit()

    def on_button_pressed(self, event):
        if event.button.id == "add_btn":
            input_widget = self.query_one("#input", Input)
            task = input_widget.value.strip()
            if task:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (task,))
                conn.commit()
                conn.close()
                input_widget.value = ""
                self.refresh_todos()

