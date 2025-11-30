# AGENTS.md Digital Dome  

> **purpose** – This file is the onboarding manual for every AI assistant (Claude, Cursor, GPT, etc.) and every human who edits this repository.

**Golden rule**: When unsure about implementation details or requirements, ALWAYS consult the developer rather than making assumptions.

---

## 0. Project overview

Placemarker is a MPA application to collect and rate various media, including but not limited to: games, movies, shows, books. The application is made so that more media types can be accommodated if needed. It is a Django application using Django templates with HTMX + AlpineJS + TailwindCSS for the frontend, SQLite as the database and Backblaze B2 for user-uploaded file storage.

---

## 1. Build, test & utility commands

The application is managed using standard Django commands and `manage.py`. Here are some useful commands:
```bash
# Start development server
python manage.py runserver
# Generate new migration files after modifying models
python manage.py makemigrations
# Apply database migrations
python manage.py migrate
```

We are using `bun` as the package manager for the frontend dependencies. There are 2 commands you should be aware of:
```bash
# Watch & build frontend assets
bun run watch
# Compile frontend assets once
bun run compile
```

---

## 2. Coding standards

* **Python**: Use type hinting whenever possible
* **DaisyUI**: Use DaisyUI components where possible to maintain consistent styling

---

## 3. Project layout & Core Components

| Directory             | Description                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------- |
| `digitaldome/`        | Django settings, views that do not fit any domain logic                                       |
| `digitaldome/common/` | Reusable components (e.g., template tags, filters) that do not fit any specific app's domain  |
| `entities/`           | Django app for media entities (games, movies, etc.) logic                                     |
| `users/`              | Django app for user management (profiles, authentication, etc.)                               |
| `tracking`            | Django app for tracking user interactions with media entities (status, ratings)               |

---

## 4. Anchor comments

Add specially formatted comments throughout the codebase, where appropriate, for yourself as inline knowledge that we can easily `grep` for.

### Guidelines:

- Use `AIDEV-NOTE:`, `AIDEV-TODO:`, or `AIDEV-QUESTION:` (all-caps prefix) for comments aimed at AI and developers.
- Keep them concise (≤ 120 chars).
- **Important:** Before scanning files, always first try to **locate existing anchors** `AIDEV-*` in relevant subdirectories.
- **Update relevant anchors** when modifying associated code.
- **Do not remove `AIDEV-NOTE`s** without explicit human instruction.
- Make sure to add relevant anchor comments, whenever a file or piece of code is:
  * too long, or
  * too complex, or
  * very important, or
  * confusing, or
  * could have a bug unrelated to the task you are currently working on.
```

---

## 5. Common pitfalls

---

## 6. Domain-Specific Terminology

---

## AI Assistant Workflow: Step-by-Step Methodology

When responding to user instructions, the AI assistant (Claude, Cursor, GPT, etc.) should follow this process to ensure clarity, correctness, and maintainability:

1. **Consult Relevant Guidance**: When the user gives an instruction, consult the relevant instructions from `AGENTS.md` file.
2. **Clarify Ambiguities**: Based on what you could gather, see if there's any need for clarifications. If so, ask the user targeted questions before proceeding.
3. **Break Down & Plan**: Break down the task at hand and chalk out a rough plan for carrying it out, referencing project conventions and best practices.
4. **Trivial Tasks**: If the plan/request is trivial, go ahead and get started immediately.
5. **Non-Trivial Tasks**: Otherwise, present the plan to the user for review and iterate based on their feedback.
6. **Track Progress**: Use a to-do list (internally, or optionally in a `TODOS.md` file) to keep track of your progress on multi-step or complex tasks.
7. **If Stuck, Re-plan**: If you get stuck or blocked, return to step 3 to re-evaluate and adjust your plan.
8. **Update Documentation**: Once the user's request is fulfilled, update relevant anchor comments (`AIDEV-NOTE`, etc.) and `AGENTS.md` files in the files and directories you touched.
9. **User Review**: After completing the task, ask the user to review what you've done, and repeat the process as needed.
10. **Session Boundaries**: If the user's request isn't directly related to the current context and can be safely started in a fresh session, suggest starting from scratch to avoid context confusion.
