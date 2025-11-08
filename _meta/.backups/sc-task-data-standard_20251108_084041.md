
---
title: symphony-core-task-data-standard
version: 1.0
author: Symphony Core Systems Team
last_updated: 2025-08-05
category: reference
tags: [task-model, interoperability, standards]
status: draft
reviewers: [rohit-anand]
next_review: 2026-02-05
---

![Draft](https://img.shields.io/badge/status-draft-lightgrey)

# Symphony Core Task Data Standard

## Purpose

Define a universal task data structure and lifecycle model to enable interoperability across ClickUp and other systems such as Notion, Jira, n8n, or custom tools.

## Scope

Applicable to all task-related data structures used in client delivery, automation, and system integration within the Symphony Core ecosystem.

## 1. Standard Task Status Model

Defines lifecycle states of a task, independent of platform:

- `TODO`: Task is created but not yet started.
- `IN PROGRESS`: Task is actively being worked on.
- `BLOCKED`: Task is unable to proceed due to a dependency.
- `REVIEW`: Task is completed and pending verification.
- `COMPLETE`: Task is done and validated.
- `CANCELLED`: Task is no longer applicable.

## 2. Standard Task Fields

Core data attributes present in any interoperable task format:

- **Task ID** – Unique identifier  
- **Title** – Human-readable task name  
- **Description** – Detailed scope of work  
- **Status** – Current lifecycle state (from above model)  
- **Assignee** – Responsible owner  
- **Creator** – Original task creator  
- **Start Date** – Planned or actual start  
- **Due Date** – Expected completion date  
- **Completion Date** – Actual completion date  
- **Priority** – One of: Low, Medium, High, Critical  
- **Tags** – Freeform labels for filtering and grouping  
- **Relationships** – Dependencies or related tasks (e.g., parent, subtask, blocked by)  
- **Estimate** – Time or effort estimate  
- **Time Tracked** – Actual time logged  

## 3. Task Relationship Types

Defines relational structure for managing hierarchy and dependencies:

- `Parent → Subtask`
- `Blocked By → Blocking`
- `Follows → Precedes`
- `Duplicate Of → Original`
- `Related To`

## 4. Standard Workflow Transitions

Abstracted state transition logic:

```text
TODO → IN PROGRESS → REVIEW → COMPLETE
             ↓
         BLOCKED
             ↓
         CANCELLED
````

Each transition must log:

* Actor (who performed it)
* Timestamp
* Optional note or reason

