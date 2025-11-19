import tempfile
from pathlib import Path
from app.storage import JSONStore
from app.models import Task, Note


def test_save_and_load_task(tmp_path):
    p = tmp_path / 'data.json'
    store = JSONStore(p)
    t = Task(title='Test task')
    store.save_task(t)

    tasks = store.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Test task'


def test_delete_task(tmp_path):
    p = tmp_path / 'data.json'
    store = JSONStore(p)
    t = Task(title='To delete')
    store.save_task(t)
    store.delete_task(t.id)
    tasks = store.list_tasks()
    assert len(tasks) == 0


def test_save_and_load_note(tmp_path):
    p = tmp_path / 'data.json'
    store = JSONStore(p)
    n = Note(title='Note 1', content='content')
    store.save_note(n)
    notes = store.list_notes()
    assert len(notes) == 1
    assert notes[0].title == 'Note 1'


def test_delete_note_cleans_task_links(tmp_path):
    p = tmp_path / 'data.json'
    store = JSONStore(p)
    t = Task(title='With note')
    store.save_task(t)
    n = Note(title='Note', linked_task_ids=[t.id])
    store.save_note(n)
    store.delete_note(n.id)
    tasks = store.list_tasks()
    assert all(n.id not in task.linked_note_ids for task in tasks)
