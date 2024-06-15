from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


def current_time_formatted() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class Todo(BaseModel):
    """
    A model representing a todo item.

    This class defines a `Todo` item with various attributes such as name,
    creation date, completion date, and due date. It also includes a validator
    for ensuring the due date is in the correct format (YYYY-MM-DD).

    Attributes
    ----------
    name : str
        The name or description of the todo item.
    created_at : str
        The timestamp when the todo item was created, defaulting to the current time.
    completed_at : Optional[str]
        The timestamp when the todo item was completed, if applicable.
    due_date : Optional[str]
        The due date for the todo item, if applicable, in the format YYYY-MM-DD.

    Methods
    -------
    validate_date_format(due_date_value: Optional[str]) -> Optional[str]
        Validates that the due date, if provided, is in the correct format (YYYY-MM-DD).
    """

    name: str
    created_at: str = Field(default_factory=current_time_formatted)
    completed_at: Optional[str] = None
    due_date: Optional[str] = None

    @field_validator("due_date")
    @classmethod
    def validate_date_format(cls, due_date_value: Optional[str]) -> Optional[str]:
        """
        Validate the format of the due date.

        Ensures that the due date, if provided, is in the correct format (YYYY-MM-DD).

        Parameters
        ----------
        due_date_value : Optional[str]
            The due date to be validated.

        Returns
        -------
        Optional[str]
            The validated due date, if provided.

        Raises
        ------
        ValueError
            If the due date is not in the correct format (YYYY-MM-DD).
        """
        if due_date_value is not None:
            try:
                datetime.strptime(due_date_value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in the format YYYY-MM-DD")

        return due_date_value


class Todos(BaseModel):
    todos: list[Todo]


def fetch_todo(todos: Todos, id: int) -> Optional[Todo]:
    """
    Fetch a todo item by its index from a Todos object.

    This function retrieves a `Todo` item from a `Todos` object based on the
    provided index. If the index is valid and corresponds to an item in the
    list, the function returns the `Todo` item; otherwise, it returns `None`.

    Parameters
    ----------
    todos : Todos
        The `Todos` object containing a list of `Todo` items.
    id : int
        The index of the `Todo` item to be retrieved from the list.

    Returns
    -------
    Optional[Todo]
        The `Todo` item if the index is valid; otherwise, `None`.
    """
    for index, todo in enumerate(todos.todos):
        if index == id:
            return todo

    return None
