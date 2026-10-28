import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import todo  # noqa: E402


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "todo.json")


def test_list_empty_when_file_missing(db):
    assert todo.list_todos(db) == []


def test_add_creates_file_and_assigns_ids(db):
    first = todo.add_todo("buy milk", db)
    second = todo.add_todo("walk dog", db)
    assert first == {"id": 1, "task": "buy milk"}
    assert second["id"] == 2
    with open(db, encoding="utf-8") as f:
        assert json.load(f) == [first, second]


def test_add_rejects_empty_task(db):
    with pytest.raises(ValueError):
        todo.add_todo("   ", db)


def test_add_supports_unicode(db):
    todo.add_todo("ซื้อนม", db)
    assert todo.list_todos(db)[0]["task"] == "ซื้อนม"


def test_remove_deletes_task(db):
    todo.add_todo("a", db)
    todo.add_todo("b", db)
    removed = todo.remove_todo(1, db)
    assert removed["task"] == "a"
    assert todo.list_todos(db) == [{"id": 2, "task": "b"}]


def test_remove_missing_raises(db):
    with pytest.raises(KeyError):
        todo.remove_todo(99, db)


def test_ids_not_reused_after_remove(db):
    todo.add_todo("a", db)
    todo.add_todo("b", db)
    todo.remove_todo(1, db)
    assert todo.add_todo("c", db)["id"] == 3


def test_cli_add_list_remove(db, capsys):
    assert todo.main(["--file", db, "add", "write", "tests"]) == 0
    assert "Added #1: write tests" in capsys.readouterr().out

    assert todo.main(["--file", db, "list"]) == 0
    assert "1. write tests" in capsys.readouterr().out

    assert todo.main(["--file", db, "remove", "1"]) == 0
    assert "Removed #1" in capsys.readouterr().out

    assert todo.main(["--file", db, "list"]) == 0
    assert "No tasks." in capsys.readouterr().out


def test_cli_remove_missing_returns_error(db, capsys):
    assert todo.main(["--file", db, "remove", "5"]) == 1
    assert "no task with id 5" in capsys.readouterr().err


def test_cli_add_empty_returns_error(db, capsys):
    assert todo.main(["--file", db, "add", " "]) == 1
    assert "must not be empty" in capsys.readouterr().err
