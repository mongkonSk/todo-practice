"""Simple command-line todo list stored in a JSON file."""

import argparse
import json
import os
import sys

DEFAULT_FILE = "todo.json"


def load_todos(path=DEFAULT_FILE):
    """Return the list of todos stored at path, or an empty list."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return []
    return json.loads(content)


def save_todos(todos, path=DEFAULT_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(task, path=DEFAULT_FILE):
    """Add a task and return the new todo item."""
    task = task.strip()
    if not task:
        raise ValueError("Task must not be empty")
    todos = load_todos(path)
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = {"id": next_id, "task": task}
    todos.append(todo)
    save_todos(todos, path)
    return todo


def remove_todo(todo_id, path=DEFAULT_FILE):
    """Remove the todo with todo_id and return it. Raises KeyError if missing."""
    todos = load_todos(path)
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos, path)
            return removed
    raise KeyError(todo_id)


def list_todos(path=DEFAULT_FILE):
    return load_todos(path)


def build_parser():
    parser = argparse.ArgumentParser(description="Simple todo list")
    parser.add_argument(
        "--file", default=DEFAULT_FILE, help="path to the JSON data file"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="add a new task")
    add_p.add_argument("task", nargs="+", help="task description")

    remove_p = sub.add_parser("remove", help="remove a task by id")
    remove_p.add_argument("id", type=int, help="id of the task to remove")

    sub.add_parser("list", help="show all tasks")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.command == "add":
        try:
            todo = add_todo(" ".join(args.task), args.file)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"Added #{todo['id']}: {todo['task']}")
    elif args.command == "remove":
        try:
            todo = remove_todo(args.id, args.file)
        except KeyError:
            print(f"Error: no task with id {args.id}", file=sys.stderr)
            return 1
        print(f"Removed #{todo['id']}: {todo['task']}")
    elif args.command == "list":
        todos = list_todos(args.file)
        if not todos:
            print("No tasks.")
        for todo in todos:
            print(f"{todo['id']}. {todo['task']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
