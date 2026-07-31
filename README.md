# Claude Code Mastery Course

A beginner-friendly, hands-on course covering Claude Code end to end — from the absolute basics to shipping a full-stack feature straight from a Jira ticket into a GitHub pull request, using nothing but natural-language prompts.

This repo holds the companion code for the course: three hands-on projects built live, from a simple snake game to a full-stack app shipped straight from Jira tickets.

---

## About This Course

Claude Code is Anthropic's AI coding agent — it reads your codebase, writes and modifies code, runs terminal commands, tests, and even deploys, all driven by plain-English prompts. Think of it less like autocomplete and more like a software engineer working alongside you.

This course walks through:

- **The fundamentals** — what Claude Code is, how it rose from an internal Anthropic project (Sept 2024) to a platform with a $2.5B+ revenue run-rate (May 2026), and how it compares to Codex CLI, Gemini CLI, and Cursor.
- **Every interface** — Claude Desktop, the VS Code extension, and the Claude CLI (the most powerful of the three).
- **Core concepts** — tokens, context windows, and session management (`/context`, `/compact`, `/clear`).
- **Extending Claude Code** — MCP servers, Skills, Plugins, and Hooks, and when to use each.
- **A real end-to-end project** — connecting Jira and GitHub via MCP, and letting Claude read a ticket, build the feature, test it, and open a pull request on its own.

## What's in This Repo

```
claude_code_course/
├── 01_snake_game/          Single-file HTML/CSS/JS game, built with Claude Desktop
├── 02_weather_app/          Streamlit + Python weather app, built with the VS Code extension & CLI
└── 03_resume_analyzer/      Full-stack end-to-end project (FastAPI + React + SQLite + Gemini API)
```

## Hands-On Projects

- **Snake Game** — a classic snake game with arrow-key controls, generated end to end from a single prompt in Claude Desktop.
- **Weather App** — a Streamlit + Python app with current conditions and a 7-day forecast, built and iteratively refined through the VS Code extension.
- **Resume Analyzer** — the course's capstone: a full-stack app (FastAPI backend, React/Vite frontend, SQLite database, Gemini API) built entirely by Claude Code from three Jira tickets, each shipped as its own reviewed GitHub pull request.

### The 3 Jira Tickets Behind the Capstone

| Ticket | Description | Acceptance Criteria |
|---|---|---|
| **1. Project Scaffolding** | FastAPI backend + React (Vite) frontend, wired with a `/api/ping-gemini` smoke-test endpoint calling the Gemini API. No database work yet. | Backend runs via `uvicorn`, frontend via `npm run dev`; the frontend button returns a live Gemini response; `.env.example` has a `GEMINI_API_KEY` placeholder, real key excluded from git. |
| **2. Resume + JD → Analysis Report** | Upload a resume (PDF or Markdown) and a job description; backend extracts the resume text, sends both to Gemini, and returns a fitment score plus recommendations. | Accepts `.pdf`/`.md` resumes and pasted JD text; response includes a score and recommendations; bad file type / empty JD / Gemini failure all show a clear frontend error. |
| **3. Persist Results to SQLite** | Save every analysis (resume text, JD text, score, recommendations, timestamp) to SQLite, and add a way to browse past analyses. | Results are written immediately after each analysis; a GET endpoint (and basic UI) lists past analyses with scores and timestamps; the database file is created automatically on first run. |

## Course Flow at a Glance

1. What Claude Code is, its rise, and how it compares to other AI coding tools
2. Setting up and comparing all three interfaces — Claude Desktop, VS Code, CLI
3. Understanding tokens and the context window
4. Documenting a project the right way — README, `CLAUDE.md`, `AGENTS.md`, and using Rewind
5. Extending Claude Code — MCP servers, Skills, Plugins, and Hooks, with hands-on demos of each
6. The capstone — wiring up Jira and GitHub via MCP and shipping a full-stack app from tickets to merged PRs
7. Best practices to carry into real projects

## Key Commands Used

**Claude CLI basics**

```bash
claude                     # launch Claude Code in the current folder
claude --resume            # resume a previous session
```

```
/init        # generate a CLAUDE.md project-context file
/context     # show context window usage
/compact     # compact the current context
/clear       # clear the current chat history
/model       # view or switch the active model
/config      # configuration, account status, and usage stats
/rename      # rename the current session
```

**MCP servers**

```bash
# context7 — always up-to-date library/API docs
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
claude mcp remove context7

# explicit scopes: local (default) / project (shared via git) / user (all projects)
claude mcp add context7 -- npx -y @upstash/context7-mcp -s local
claude mcp add context7 -- npx -y @upstash/context7-mcp -s project
claude mcp add context7 -- npx -y @upstash/context7-mcp -s user

# GitHub MCP server (fine-grained personal access token)
claude mcp add --transport http github https://api.githubcopilot.com/mcp --header "Authorization: Bearer <Your token>"

# Jira / Atlassian MCP server (OAuth on first use, no token needed here)
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
```

```
/mcp    # list configured MCP servers and connection status
```

**Skills & Plugins**

```bash
# install a skill from a marketplace
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser
```

```
/skills         # list installed skills and their token footprint
/plugin         # discover, install, and manage plugins
/feature-dev    # run the structured feature-development workflow (a plugin command)
```

**Hooks & permissions**

```
/hooks          # list supported hook events
/permissions    # view and edit granted tool permissions
```

```bash
# bypasses ALL permission prompts — only ever use in a disposable VM/container
claude --dangerously-skip-permissions
```

## Prerequisites & Getting Started

- A [Claude](https://claude.ai) **Pro** plan or higher (Claude Code is not available on the free tier)
- [Claude Desktop](https://claude.ai/download) and/or [VS Code](https://code.visualstudio.com/) with the official **Claude Code** extension
- Node.js (for MCP servers and skills installed via `npx`), Python 3.9+ for the weather app and resume analyzer backend

## Connect

Questions or feedback on the course — drop a comment on the video or open an issue in this repo.
