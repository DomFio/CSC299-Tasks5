from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
from .models import Task, Note


class JSONStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({'tasks': [], 'notes': []})

    def _read(self) -> Dict[str, Any]:
        try:
            with self.path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # preserve corrupted file
            corrupt = self.path.with_suffix(self.path.suffix + '.corrupt')
            self.path.rename(corrupt)
            # create new empty store
            self._write({'tasks': [], 'notes': []})
            return {'tasks': [], 'notes': []}

    def _write(self, data: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(self.path.suffix + '.tmp')
        with tmp.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(self.path)

    def list_tasks(self) -> List[Task]:
        data = self._read()
        return [Task(**t) for t in data.get('tasks', [])]

    def list_notes(self) -> List[Note]:
        data = self._read()
        return [Note(**n) for n in data.get('notes', [])]

    def save_task(self, task: Task) -> None:
        data = self._read()
        tasks = data.get('tasks', [])
        ids = [t['id'] for t in tasks]
        if task.id in ids:
            # replace
            tasks = [task.__dict__ if t['id'] == task.id else t for t in tasks]
        else:
            tasks.append(task.__dict__)
        data['tasks'] = tasks
        self._write(data)

    def delete_task(self, task_id: str) -> None:
        data = self._read()
        tasks = [t for t in data.get('tasks', []) if t['id'] != task_id]
        # also remove references from notes
        notes = data.get('notes', [])
        for n in notes:
            if task_id in n.get('linked_task_ids', []):
                n['linked_task_ids'] = [tid for tid in n.get('linked_task_ids', []) if tid != task_id]
        data['tasks'] = tasks
        data['notes'] = notes
        self._write(data)

    def save_note(self, note: Note) -> None:
        data = self._read()
        notes = data.get('notes', [])
        ids = [n['id'] for n in notes]
        if note.id in ids:
            notes = [note.__dict__ if n['id'] == note.id else n for n in notes]
        else:
            notes.append(note.__dict__)
        data['notes'] = notes
        self._write(data)

    def delete_note(self, note_id: str) -> None:
        data = self._read()
        notes = [n for n in data.get('notes', []) if n['id'] != note_id]
        # remove references from tasks
        tasks = data.get('tasks', [])
        for t in tasks:
            if note_id in t.get('linked_note_ids', []):
                t['linked_note_ids'] = [nid for nid in t.get('linked_note_ids', []) if nid != note_id]
        data['notes'] = notes
        data['tasks'] = tasks
        self._write(data)
