from __future__ import annotations

import argparse
from pathlib import Path
from .storage import JSONStore
from .models import Task, Note
import sys


def _print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks")
        return
    for t in tasks:
        print(f"- {t.id} | {t.title} | {t.status} | tags:{','.join(t.tags)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="taskmgr")
    parser.add_argument('--data', '-d', help='path to data file', default='~/.taskmgr/data.json')
    sub = parser.add_subparsers(dest='cmd')

    add = sub.add_parser('add', help='add a task')
    add.add_argument('title')
    add.add_argument('--desc', '-m', help='description', default='')

    ls = sub.add_parser('list', help='list tasks')
    ls.add_argument('--status', choices=['open', 'in-progress', 'done'], help='filter by status')

    upd = sub.add_parser('update', help='update a task')
    upd.add_argument('id')
    upd.add_argument('--title')
    upd.add_argument('--desc')
    upd.add_argument('--status', choices=['open', 'in-progress', 'done'])

    rm = sub.add_parser('delete', help='delete a task')
    rm.add_argument('id')

    note = sub.add_parser('note', help='manage notes')
    note_sub = note.add_subparsers(dest='note_cmd')
    note_add = note_sub.add_parser('add')
    note_add.add_argument('title')
    note_add.add_argument('--content', '-c', default='')
    note_add.add_argument('--link-task')

    args = parser.parse_args(argv)
    data_file = Path(args.data).expanduser()
    store = JSONStore(data_file)

    if args.cmd == 'add':
        t = Task(title=args.title, description=args.desc)
        store.save_task(t)
        print(t.id)
        return 0

    if args.cmd == 'list':
        tasks = store.list_tasks()
        if args.status:
            tasks = [t for t in tasks if t.status == args.status]
        _print_tasks(tasks)
        return 0

    if args.cmd == 'update':
        tasks = store.list_tasks()
        task = next((t for t in tasks if t.id == args.id), None)
        if not task:
            print('Task not found', file=sys.stderr)
            return 2
        if args.title:
            task.title = args.title
        if args.desc:
            task.description = args.desc
        if args.status:
            task.status = args.status
        task.touch()
        store.save_task(task)
        print('updated')
        return 0

    if args.cmd == 'delete':
        store.delete_task(args.id)
        print('deleted')
        return 0

    if args.cmd == 'note' and args.note_cmd == 'add':
        n = Note(title=args.title, content=args.content)
        if args.link_task:
            n.linked_task_ids.append(args.link_task)
        store.save_note(n)
        print(n.id)
        return 0

    parser.print_help()
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
