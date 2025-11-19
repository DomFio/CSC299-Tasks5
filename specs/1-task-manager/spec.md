# Feature Specification: Task Manager

**Feature Branch**: `1-task-manager`  
**Created**: 2025-11-19  
**Status**: Draft  
**Input**: User description: "I want to create a python program that is a task manager. That allows you to create new tasks, delete and update. create knowledge notes. and stores data locally to JSON files."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Manage Tasks (Priority: P1)

As a user, I want to create, view, update, and delete tasks locally so I can track my work without relying on remote services.

**Why this priority**: Core functionality. Without CRUD for tasks the product provides no primary value.

**Independent Test**: Create a new task, verify it appears in the task list, update its fields, and delete it; verify persistence in the local JSON store across program restarts.

**Acceptance Scenarios**:

1. **Given** the program is running with an empty store, **When** a user creates a new task with title and optional description, **Then** the task is saved to local JSON and appears in the task list.
2. **Given** a task exists, **When** the user updates its title/description/status, **Then** the changes are persisted and visible.
3. **Given** a task exists, **When** the user deletes it, **Then** it is removed from the JSON store and no longer shown in the list.

---

### User Story 2 - Knowledge Notes (Priority: P2)

As a user, I want to create knowledge notes linked to tasks or standalone so I can capture context and decisions.

**Why this priority**: Adds valuable context for tasks and supports knowledge capture, but not required for basic task tracking.

**Independent Test**: Create a note, link it to a task, verify note content and link persist in JSON store.

**Acceptance Scenarios**:

1. **Given** the program is running, **When** the user creates a new knowledge note and links it to a task ID, **Then** the note is stored with the task reference in JSON.
2. **Given** a note exists, **When** the user edits the note, **Then** the updated content is persisted.
3. **Given** a note exists, **When** the user deletes the note, **Then** it is removed from the store and task references are updated.

---

### User Story 3 - Local Persistence & Portability (Priority: P3)

As a user, I want the data stored in JSON files so I can back up or move my data easily.

**Why this priority**: Portability and transparency are important for a local tool but secondary to CRUD flows.

**Independent Test**: Inspect JSON files on disk after operations; copy files and open on another machine to verify tasks load.

**Acceptance Scenarios**:

1. **Given** tasks exist and are persisted, **When** the program restarts, **Then** tasks load from the JSON store.
2. **Given** JSON files are copied to another machine, **When** the program points to those files, **Then** tasks and notes import successfully.

---

### Edge Cases

- What happens when the JSON store is corrupted? The program SHOULD detect corruption, back up the bad file to a `*.corrupt.timestamp` file and create a new empty store, while notifying the user.
- How does the system handle concurrent writes? The program SHOULD use simple file locking to prevent race conditions when multiple processes access the same store.
- Large numbers of tasks (10k+): The program SHOULD remain operable; performance expectations are documented in assumptions.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create tasks with at least a title and optional description, due date, status (open/in-progress/done), and tags.
- **FR-002**: System MUST allow users to list tasks, filter by status, tag, and search by title.
- **FR-003**: System MUST allow users to update task fields and persist changes to the JSON store.
- **FR-004**: System MUST allow users to delete tasks and remove associated references from notes.
- **FR-005**: System MUST allow users to create, edit, link, and delete knowledge notes; notes MAY be linked to zero or more tasks.
- **FR-006**: System MUST persist all tasks and notes to local JSON files in a configurable data directory.
- **FR-007**: System MUST validate input and return user-friendly errors for invalid data.
- **FR-008**: System SHOULD create automatic backups of the JSON files before destructive operations (e.g., overwrite, delete) and on startup if store modification timestamp is older than a configurable threshold.
- **FR-009**: System MUST detect JSON corruption and preserve the corrupted file as a backup before attempting recovery.
- **FR-010**: System SHOULD provide a simple CLI to execute CRUD operations and basic queries.

### Key Entities

- **Task**: Represents an actionable item. Attributes: id, title, description, due_date, status, tags, created_at, updated_at, linked_note_ids.
- **Note**: Represents a knowledge note. Attributes: id, title, content, created_at, updated_at, linked_task_ids.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can perform create/read/update/delete tasks in under 10 seconds using the CLI for basic flows.
- **SC-002**: 100% of CRUD operations persist correctly to JSON and survive a program restart in test scenarios.
- **SC-003**: Importing exported JSON files into a fresh install restores tasks and notes with >=99% fidelity in automated tests.
- **SC-004**: Corrupted JSON detection recovers by preserving corrupted file and creating a new store in >=95% of simulated corruption tests.


## Assumptions

- Single-user, local-first tool; no authentication is required.
- Target environment: Python 3.10+ on desktop OS (Windows, macOS, Linux).
- Reasonable dataset size: up to 10k tasks and 10k notes; not optimized for very large datasets.
- CI and packaging are out of scope for initial implementation.
- UI surface: CLI-only for v1 (no GUI planned).
- Concurrency model: single-user program; no file locking or multi-process concurrency guarantees are provided.

## Open Questions

- (Resolved) UI surface: CLI-only chosen for v1 (Q1: A).

- (Resolved) Concurrency model: single-user program, no locking (Q2: single-user).




