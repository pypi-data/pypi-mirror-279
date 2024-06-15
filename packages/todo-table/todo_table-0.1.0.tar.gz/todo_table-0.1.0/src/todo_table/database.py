from todo_table.todo import Todos
import json
from pathlib import Path


def write_todos_to_file(todos: Todos, todos_file: Path) -> None:
    """
    Write the todos to a file in JSON format.

    This function serializes the provided `Todos` object to a JSON string using Pydantic
    and writes it to the specified file. If an error occurs during the file
    operation, an error message is printed.

    Parameters
    ----------
    todos : Todos
        The `Todos` object containing the todos to be written to the file.
    todos_file : Path
        The path to the file where the todos should be saved as a pathlib.Path

    Returns
    -------
    None
    """
    json_string = todos.model_dump_json(warnings=True)

    with todos_file.open("w", encoding="utf-8") as file:
        file.write(json_string)


def load_todos_from_file(todos_file: Path) -> Todos:
    """
    Load todos from a JSON file.

    This function reads a JSON file from the specified path, deserializes the
    JSON content into a `Todos` object, and returns it. If the file is not
    found, or an error occurs during the file operation or JSON decoding, an
    error message is printed.

    Parameters
    ----------
    todos_file : Path
        The Path to the file from which the todos should be loaded.

    Returns
    -------
    Todos
        The `Todos` object containing the loaded todos.
    """
    try:
        with todos_file.open("r", encoding="utf-8") as file:
            todos_json = json.load(file)
    except FileNotFoundError:
        print("No todo file found, you need to add a todo!")
        raise SystemExit

    todos = Todos(**todos_json)

    return todos
