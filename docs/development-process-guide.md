---
title: Lightweight Development Process Guide
subtitle: From Idea to Delivery - A Simple Framework for Small Teams
version: 1.0
date: 2025-10-09
template: true
---

# Lightweight Development Process Guide
## A Simple Framework for Small Teams

---

## Overview

This guide explains our streamlined development process. It's designed for **small teams** (2-5 people) who want structure without bureaucracy.

**Core Principle**: Focus on the 20% of process that delivers 80% of value (Pareto Principle)

**Key Documents**:
1. **PRD** (Product Requirements Document) - What and Why
2. **Architecture Doc** - How
3. **Sprint Tracking** - Progress

---

## The Big Picture

```
┌─────────────┐
│    Idea     │  "We need to solve X problem"
└──────┬──────┘
       ↓
┌─────────────┐
│  Write PRD  │  1-2 days: Define problem, success, requirements
└──────┬──────┘
       ↓
┌─────────────┐
│ Architecture│  1-2 days: Design solution, plan implementation
└──────┬──────┘
       ↓
┌─────────────┐
│   Sprints   │  1-week cycles: Build, test, deliver
│ (Iterate)   │
└──────┬──────┘
       ↓
┌─────────────┐
│   Deliver   │  Working software in production
└─────────────┘
```

**Timeline**: Typical small project = 1-2 days planning + 2-4 weeks building

---

## Phase 1: Product Requirements Document (PRD)

### Purpose
The PRD answers:
- **What** are we building?
- **Why** are we building it?
- **Who** is it for?
- **How** do we measure success?

### When to Write
Write a PRD when:
- Starting a new project
- Adding a major feature
- Making significant changes to existing systems

Don't write a PRD for:
- Bug fixes
- Minor tweaks
- Routine maintenance

### What Goes in a PRD

#### 1. Executive Summary (2-3 paragraphs)
- Product name and vision
- One-line description
- Key success metric

**Example**:
```
Product: Symphony Core Document Management
Vision: Automated document consistency checking
One-liner: "Continuous document intelligence for small teams"
Success: Reduce review time from 4 hours/week to 15 minutes/week
```

#### 2. Problem Statement (1 page)
- Current situation
- Pain points (table format works well)
- Why we need to solve this now

**Example**:
```
Current: We manually review 50 documents weekly for conflicts
Pain: Takes 4 hours, error-prone, scales poorly
Why now: Documents growing 10+ per quarter, team shrinking
```

#### 3. Goals & Success Metrics (½ page)
- 3 clear objectives
- Measurable key results for each
- What's explicitly OUT of scope

**Example**:
```
Goal: Eliminate document contradictions
KR1: Detect 100% of pricing conflicts
KR2: Zero customer-reported issues
Out of scope: Real-time collaboration, web UI
```

#### 4. User Personas (½ page)
- 1-2 key users
- Their goals and frustrations
- How they'll use the system

#### 5. Requirements (2-3 pages)
Break into:
- **Functional Requirements**: What the system does
- **Non-Functional Requirements**: How well it does it

Use this format:
```
FR-1.1: Change Detection
- System SHALL detect new/modified files
- System SHALL use file hashing
- Acceptance Criteria:
  - Detects changes in < 1 second
  - Handles 50+ documents
```

#### 6. User Stories (1-2 pages)
Write stories in this format:
```
As a [user type]
I want [feature]
So that [benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2

Story Points: 5
```

### PRD Template

Use this structure:
```markdown
1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. User Personas
5. Functional Requirements
6. Non-Functional Requirements
7. User Stories (sprint-ready)
8. Technical Constraints
9. Dependencies & Risks
10. Timeline
11. Open Questions
12. Appendix
```

### Time Investment
- **Writing**: 4-8 hours
- **Review**: 1-2 hours
- **Updates**: As needed (rarely)

### Tips for Good PRDs
✅ **Do**:
- Be specific about success metrics
- Include acceptance criteria
- List what's OUT of scope
- Use tables and lists for clarity
- Write in present tense ("System SHALL...")

❌ **Don't**:
- Describe HOW to build it (that's for architecture)
- Use vague terms ("improve", "enhance")
- Skip acceptance criteria
- Write more than 10-15 pages

---

## Phase 2: Architecture & Solution Design

### Purpose
The Architecture Doc answers:
- **How** will we build it?
- **What** technologies will we use?
- **Why** these specific choices?

### When to Write
Write after PRD is approved, before coding starts.

### What Goes in Architecture Doc

#### 1. System Architecture (1-2 pages)
- High-level diagram showing components
- Data flow diagram
- Component interactions

**Example**:
```
[User CLI] → [Processor] → [Tagging Engine]
                ↓              ↓
           [Cache]      [Claude API]
```

#### 2. Component Design (3-4 pages)
For each major component:
- Responsibility (what it does)
- Key methods/interfaces
- Data structures
- Interactions with other components

**Example**:
```python
class DocumentProcessor:
    """Orchestrates document processing workflow"""
    
    def process_incrementally() -> Result:
        """Process only changed files"""
        
    def get_changed_files() -> List[Path]:
        """Detect file changes via hashing"""
```

#### 3. Technology Choices (1 page)
List key technologies and why:
```
Python 3.11+: Team expertise, rich ecosystem
Claude API: Best reasoning for conflicts
File-based storage: Simple, Git-friendly
```

#### 4. Data Models (1 page)
Show key data structures:
```python
@dataclass
class Document:
    filepath: Path
    content: str
    tags: List[str]
    last_modified: datetime
```

#### 5. Error Handling (½ page)
- Error categories
- Handling strategy
- Retry logic

#### 6. Performance Targets (½ page)
```
Full processing: < 10 minutes for 50 docs
Incremental: < 5 minutes
Change detection: < 1 second
```

#### 7. Security Considerations (½ page)
- API key management
- Data privacy
- Input validation

#### 8. Testing Strategy (½ page)
- Test pyramid (80% unit, 15% integration, 5% E2E)
- What to test
- Test data approach

#### 9. Deployment (½ page)
- Installation steps
- Configuration
- Operational commands

#### 10. Decision Log (ongoing)
Record major decisions:
```
Decision: Use file-based storage vs database
Date: 2025-10-09
Rationale: Scale < 100 docs, simplicity wins
Consequences: Simple but limited queries
```

### Architecture Template

```markdown
1. Document Overview
2. Architecture Principles
3. System Architecture (diagrams)
4. Component Design
5. Data Models
6. API Integration Details
7. Error Handling Strategy
8. Performance Considerations
9. Security Considerations
10. Testing Strategy
11. Deployment & Operations
12. Future Enhancements
13. Decision Log
14. Appendix
```

### Time Investment
- **Writing**: 6-10 hours
- **Review**: 2-3 hours
- **Updates**: As design evolves

### Tips for Good Architecture Docs
✅ **Do**:
- Use diagrams (they're worth 1000 words)
- Show code examples
- Explain WHY you chose technologies
- Include actual data structures
- Document decisions with rationale

❌ **Don't**:
- Document every function (that's code comments)
- Use buzzwords without substance
- Skip the "why" behind decisions
- Ignore error handling and security

---

## Phase 3: Sprint Development

### What is a Sprint?

A **sprint** is a fixed time period (usually 1 week) where you:
1. Choose work from the backlog
2. Build the features
3. Test what you built
4. Demo and review
5. Plan the next sprint

### Sprint Structure (1 Week)

```
Monday
├─ Sprint Planning (1 hour)
│  └─ Pick user stories for this week
│
Tuesday - Thursday
├─ Development
│  ├─ Write code
│  ├─ Test code
│  └─ Daily standup (15 min each day)
│
Friday
├─ Testing & Documentation (morning)
└─ Sprint Review & Planning (afternoon)
   ├─ Demo what you built
   ├─ Retrospective: What went well/poorly?
   └─ Plan next sprint
```

### Sprint Planning Meeting (Monday, 1 hour)

**Goal**: Decide what to build this week

**Process**:
1. Review last sprint (what we delivered)
2. Look at user stories in backlog
3. Estimate effort (story points)
4. Commit to stories that fit in 1 week
5. Break stories into tasks

**Story Points Guide**:
- 1 point = 1-2 hours (tiny task)
- 3 points = half day
- 5 points = 1 day
- 8 points = 2-3 days
- 13 points = full week (break it down!)

**Sprint Capacity**:
- 1 developer = ~20-25 points per week
- 2 developers = ~40-50 points per week

**Example Planning**:
```
Sprint Goal: Implement document tagging

Stories for this sprint:
- US-1.1: Change detection (5 points)
- US-1.2: YAML frontmatter (3 points)
- US-2.1: Auto-tagging system (8 points)
Total: 16 points (fits in 1 week for 1 dev)
```

### Daily Standup (15 minutes, every day)

**Three Questions**:
1. What did I do yesterday?
2. What will I do today?
3. Any blockers?

**Example**:
```
Yesterday: Implemented file change detection
Today: Start YAML frontmatter handling
Blockers: Need sample documents for testing
```

**Tips**:
- Keep it SHORT (15 minutes max)
- Don't solve problems in standup
- Take detailed discussions offline

### Sprint Review (Friday afternoon, 1 hour)

**Part 1: Demo (30 min)**
- Show working features
- Get feedback
- Update backlog if needed

**Part 2: Retrospective (30 min)**
- What went well? (keep doing)
- What went poorly? (stop doing)
- What should we try? (start doing)

**Example Retro**:
```
✅ Keep: Daily standups stayed short
❌ Stop: Leaving testing until Friday
🔄 Try: Write tests alongside code
```

### Tracking Progress

#### Simple Sprint Board

```
┌─────────────┬──────────────┬──────────────┬──────────┐
│   TO DO     │  IN PROGRESS │   TESTING    │   DONE   │
├─────────────┼──────────────┼──────────────┼──────────┤
│ US-2.1      │  US-1.1      │   US-1.2     │          │
│ US-2.2      │              │              │          │
│             │              │              │          │
└─────────────┴──────────────┴──────────────┴──────────┘
```

Use:
- Sticky notes on whiteboard, OR
- Simple markdown file, OR
- Trello/GitHub Projects (if you want digital)

#### Tracking in Markdown

Create `sprint-tracking.md`:
```markdown
# Sprint 1: Foundation (Oct 9-13, 2025)

## Sprint Goal
Implement change detection and document tagging

## Committed Stories (16 points)
- [ ] US-1.1: Change detection (5 pts) - In Progress
- [ ] US-1.2: YAML frontmatter (3 pts) - To Do  
- [ ] US-2.1: Auto-tagging (8 pts) - To Do

## Daily Updates

### Monday, Oct 9
- Sprint planned
- Started US-1.1

### Tuesday, Oct 10
- US-1.1: Completed file hashing
- US-1.1: Started cache implementation
- Blocker: Need to decide on cache format

## Sprint Retrospective
(Fill in on Friday)
```

---

## Putting It All Together

### Timeline for a Typical Project

```
Week 0: Planning
├─ Day 1-2: Write PRD
├─ Day 3: Review PRD, get approval
└─ Day 4-5: Write Architecture Doc

Week 1: Sprint 1 - Foundation
├─ Build: Core infrastructure
└─ Deliver: Basic working pieces

Week 2: Sprint 2 - Core Features
├─ Build: Main functionality
└─ Deliver: MVP working end-to-end

Week 3: Sprint 3 - Polish
├─ Build: Edge cases, refinements
└─ Deliver: Production-ready features

Week 4: Sprint 4 - Launch
├─ Test, document, deploy
└─ Deliver: In production!
```

### Document Lifecycle

```
PRD
├─ Written: Before coding
├─ Updated: When requirements change (rarely)
└─ Status: Should be stable

Architecture Doc
├─ Written: After PRD, before coding
├─ Updated: As design evolves (occasionally)
└─ Status: Living document

Sprint Tracking
├─ Created: Start of each sprint
├─ Updated: Daily
└─ Status: Very active, then archived
```

### Where Documents Live

```
project/
├─ docs/
│  ├─ product-requirements-document.md    (PRD)
│  ├─ architecture-solution-design.md     (Architecture)
│  └─ development-process.md              (This guide)
│
├─ sprints/
│  ├─ sprint-01-foundation.md
│  ├─ sprint-02-features.md
│  └─ sprint-03-polish.md
│
└─ src/
   └─ (your code)
```

---

## Quick Reference

### When to Use Each Document

| Situation | Document to Use |
|-----------|----------------|
| Starting new project | Write PRD → Architecture |
| Major feature | Write PRD (mini version) |
| Design question | Update Architecture Doc |
| Daily work tracking | Sprint tracking file |
| Bug fix | No doc, just fix it |
| Weekly planning | Sprint planning meeting |

### Document Size Guidelines

| Document | Target Length | Time to Write |
|----------|--------------|---------------|
| PRD | 8-12 pages | 4-8 hours |
| Architecture | 10-15 pages | 6-10 hours |
| Sprint Tracking | 1-2 pages | 15 min/day |

### Sprint Ceremonies Time Budget

| Activity | Frequency | Duration |
|----------|-----------|----------|
| Sprint Planning | Weekly (Monday) | 1 hour |
| Daily Standup | Daily | 15 minutes |
| Sprint Review | Weekly (Friday) | 1 hour |
| Development | Daily | Rest of the time |

---

## Common Questions

**Q: Do we really need all these documents?**  
A: For small projects (< 2 weeks), you can combine PRD + Architecture into one doc. But separate them for anything longer.

**Q: What if requirements change mid-sprint?**  
A: Finish the sprint, then update PRD and adjust next sprint. Don't change mid-sprint.

**Q: Can we skip the architecture doc?**  
A: Only for very simple projects. The architecture doc saves time by thinking through design before coding.

**Q: How do I estimate story points?**  
A: Use past experience. After a few sprints, you'll know your velocity (points per week).

**Q: What if we don't finish everything in a sprint?**  
A: That's normal! Move unfinished stories to next sprint. Focus on completing SOME things rather than starting everything.

**Q: Do we need standups if it's just 2 people?**  
A: Yes, but make them 5 minutes. It's about communication and spotting blockers early.

---

## Tips for Success

### PRD Tips
- **Start with the problem**, not the solution
- **Be specific** about success metrics
- **Include examples** in requirements
- **List what's OUT** of scope

### Architecture Tips
- **Draw diagrams** - visualize before coding
- **Explain WHY** you chose each technology
- **Show code examples** of key interfaces
- **Document decisions** in the decision log

### Sprint Tips
- **Keep sprints short** (1 week is ideal)
- **Deliver something** every sprint
- **Don't overcommit** - better to finish less
- **Test as you go** - don't leave it until Friday
- **Update tracking daily** - takes 2 minutes

### Team Tips
- **Communicate constantly**
- **Ask for help** when blocked
- **Demo frequently** - even incomplete work
- **Celebrate small wins**
- **Learn from mistakes** in retrospectives

---

## Checklist: Starting a New Project

Use this checklist when starting any new project:

### Planning Phase (Week 0)
- [ ] Understand the problem clearly
- [ ] Write PRD using template
- [ ] Get PRD reviewed and approved
- [ ] Write Architecture Doc using template
- [ ] Get Architecture Doc reviewed
- [ ] Break work into user stories
- [ ] Estimate story points
- [ ] Set up project structure

### Sprint Setup
- [ ] Create sprint tracking document
- [ ] Schedule sprint ceremonies (planning, standup, review)
- [ ] Set up development environment
- [ ] Create initial sprint backlog

### During Development
- [ ] Hold daily standups (15 min)
- [ ] Update sprint tracking daily
- [ ] Write tests alongside code
- [ ] Document as you build
- [ ] Demo frequently

### Sprint End
- [ ] Complete testing
- [ ] Update documentation
- [ ] Demo working features
- [ ] Hold retrospective
- [ ] Plan next sprint

---

## Adapting This Process

This process is a **starting point**. Adapt it to your team:

**For Solo Developers**:
- Skip standups (but still track daily)
- Shorter sprint reviews (demo to yourself!)
- Still do retrospectives (learn from yourself)

**For 2-Person Teams**:
- Keep all ceremonies but shorter
- Rotate who leads meetings
- Pair programming on complex features

**For 3-5 Person Teams**:
- Follow this process as-is
- Consider a rotating "sprint lead"
- Add code review process

**For Larger Teams** (6+):
- You need more process than this
- Consider full Scrum or Kanban
- Add dedicated project manager

---

## Tools You Might Need

### Minimum (Free)
- Text editor (VSCode, Sublime)
- Markdown files for documentation
- Sticky notes or whiteboard for sprint board
- Git for version control

### Nice to Have (Free/Cheap)
- Trello or GitHub Projects (sprint board)
- Slack or Discord (team communication)
- GitHub/GitLab (code + documentation)

### Skip These (Too Heavy for Small Teams)
- JIRA (overkill for small teams)
- Confluence (use markdown files instead)
- Microsoft Project (way too complex)

---

## Templates

### PRD Template (Shortened)
```markdown
# Product Requirements Document

## 1. Executive Summary
[Product vision, one-liner, success metric]

## 2. Problem Statement
[Current situation, pain points, why now]

## 3. Goals & Success Metrics
[3 objectives with measurable KRs]

## 4. User Personas
[1-2 key users with goals]

## 5. Requirements
[Functional and non-functional requirements]

## 6. User Stories
[Sprint-ready stories with acceptance criteria]

## 7. Appendix
[Supporting details, examples]
```

### Architecture Template (Shortened)
```markdown
# Architecture & Solution Design

## 1. System Architecture
[Diagrams showing components and data flow]

## 2. Component Design
[For each component: purpose, methods, interactions]

## 3. Technology Choices
[What and why for each major technology]

## 4. Data Models
[Key data structures]

## 5. Error Handling
[Strategy and implementation]

## 6. Testing Strategy
[What and how to test]

## 7. Deployment
[How to install and run]

## 8. Decision Log
[Record major decisions]
```

### Sprint Tracking Template
```markdown
# Sprint N: [Name] ([Dates])

## Sprint Goal
[What we're trying to achieve this week]

## Committed Stories ([X] points)
- [ ] Story 1 (points) - Status
- [ ] Story 2 (points) - Status

## Daily Log
### [Date]
[What happened today]

## Blockers
[Current blockers and resolution plan]

## Sprint Retrospective
### What Went Well
### What Didn't Go Well  
### What to Try Next Sprint
```

---

## Summary

**Remember the core flow**:
1. **PRD**: What and Why
2. **Architecture**: How
3. **Sprints**: Build it

**Keep it simple**:
- Write just enough documentation
- Track progress daily
- Deliver working software weekly
- Improve continuously

**Most important**:
- **Communication** over documentation
- **Working software** over perfect plans
- **Feedback** over following the process

Good luck! 🚀

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-09  
**Status**: Living Template
