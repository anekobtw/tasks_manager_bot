import sqlite3


class DBManager:
    def __init__(self, db_name: str, table_schema: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute(table_schema)
        self.connection.commit()

    def execute_query(self, query: str, params: tuple = ()) -> None:
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()


class CategoryManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            category_name TEXT
        )"""
        super().__init__("database/category.db", table_schema)

    def create_category(self, category_name: str) -> None:
        self.execute_query("INSERT INTO category(category_name) VALUES (?)", (category_name,))

    def delete_category(self, category_id: int) -> None:
        self.execute_query("DELETE FROM category WHERE category_id = ?", (category_id,))

    def find_category(self, category_id: int) -> list:
        return self.fetch_one("SELECT * FROM category WHERE category_id = ?", (category_id,))

    def get_all_categories(self) -> list:
        return self.fetch_all("SELECT * FROM category")


class TasksManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            task_name TEXT,
            category_id INTEGER,
            task_status INTEGER
        )"""
        super().__init__("database/tasks.db", table_schema)

    def create_task(self, task_name: str, category_id: int, task_status: int) -> None:
        cm = CategoryManager()
        if cm.find_category(category_id):
            self.execute_query("INSERT INTO tasks(task_name, category_id, task_status) VALUES (?, ?, ?)", (task_name, category_id, task_status))

    def delete_task(self, task_id: int) -> None:
        self.execute_query("DELETE FROM tasks WHERE task_id = ?", (task_id,))

    def set_status(self, task_id: int, new_status: int) -> None:
        self.execute_query("UPDATE tasks SET task_status = ? WHERE task_id = ?", (new_status, task_id))

    def find_task(self, task_id: int) -> list:
        return self.fetch_one("SELECT * FROM tasks WHERE task_id = ?", (task_id,))

    def get_all_tasks(self) -> list:
        return self.fetch_all("SELECT * FROM tasks")

    def get_tasks_by_category(self, category_id: int) -> list:
        return self.fetch_all("SELECT task_id, task_name, task_status FROM tasks WHERE category_id = ?", (category_id,))
