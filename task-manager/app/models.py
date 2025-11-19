from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + 'Z'


@dataclass
class Note:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    linked_task_ids: List[str] = field(default_factory=list)

    def touch(self) -> None:
        self.updated_at = _now_iso()


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    due_date: Optional[str] = None
    status: str = "open"  # open, in-progress, done
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    linked_note_ids: List[str] = field(default_factory=list)

    def touch(self) -> None:
        self.updated_at = _now_iso()
