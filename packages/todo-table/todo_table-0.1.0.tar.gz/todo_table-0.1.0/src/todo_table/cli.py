from typing import Optional
import fire

# from todo_table.todo import Todo, Todos, current_time_formatted, fetch_todo
from todo_table import todo

# from todo_table.database import write_todos_to_file, load_todos_from_file
from todo_table import database
from pathlib import Path
from prettytable import PrettyTable


class TodoTableCLI:
    def init(self, database_file: str | Path = Path.home() / "todo_table.json") -> None:
        database_file = Path(database_file)
        init_todos = todo.Todos(todos=[])
        database.write_todos_to_file(todos=init_todos, todos_file=database_file)
        print(f"todotable successfully initialized at {database_file}")

    def add(
        self,
        name: str,
        due: Optional[str] = None,
        database_file: str | Path = Path.home() / "todo_table.json",
    ) -> None:
        database_file = Path(database_file)
        todo_to_add = todo.Todo(name=name, due_date=due)

        todos = database.load_todos_from_file(todos_file=database_file)
        todos.todos.append(todo_to_add)

        database.write_todos_to_file(todos=todos, todos_file=database_file)

    def done(
        self, id: int, database_file: str | Path = Path.home() / "todo_table.json"
    ) -> Optional[todo.Todo]:
        database_file = Path(database_file)
        offset_id = id - 1  # to offset adding 1 to the index in show
        todos = database.load_todos_from_file(todos_file=database_file)
        fetched_todo = todo.fetch_todo(todos=todos, id=offset_id)
        if fetched_todo is not None:
            del todos.todos[offset_id]
            print(f"Todo {fetched_todo.name} completed")
            database.write_todos_to_file(todos=todos, todos_file=database_file)
            return fetched_todo
        else:
            print(f"No todo with ID {str(id)} found")
            return None

    def show(self, database_file: str | Path = Path.home() / "todo_table.json") -> None:
        database_file = Path(database_file)
        table = PrettyTable()
        table.field_names = ["Id", "Name", "Created At", "Completed At", "Due Date"]

        todos = database.load_todos_from_file(todos_file=database_file)

        for index, to_do in enumerate(todos.todos):
            table_index = index + 1  # so the ids start at 1
            table.add_row(
                [
                    table_index,
                    to_do.name,
                    to_do.created_at,
                    to_do.completed_at,
                    to_do.due_date,
                ]
            )

        print(table)


def cli() -> None:
    todo_table = TodoTableCLI()
    fire.Fire(todo_table)
