# AGENTS.md

Instructions for coding agents (Claude Code, Cursor, Codex, and others) helping someone set up and try this repository. The goal: from a fresh clone to watching Claude drive a browser on a task the user picked, in a few minutes, with the user in control of their credentials.

This repository shows how to give Claude a browser through the Anthropic SDK. `StagehandBrowser`, from the `stagehand-claude-sdk` package, implements Anthropic's browser toolset on top of Stagehand. The Anthropic tool runner handles the model loop. There is one example per language:

| | TypeScript | Python |
| --- | --- | --- |
| Directory | `typescript/` | `python/` |
| Example | `typescript/example.ts` | `python/example.py` |
| Requires | Node.js 22.18+, pnpm | Python 3.13+, uv |
| Run | `pnpm example` | `uv run --env-file .env python example.py` |

## How to work with the user

- **Do the work, ask only for decisions.** Run the checks and installs yourself. Ask the user only about what is theirs to decide: the language, local Chrome or Browserbase, their API keys, and the task to try.
- **Never read, print, or paste secrets.** Don't `cat` a `.env` file or echo key values. Ask the user to paste keys into `.env` themselves, then check that a key is present without showing it (see step 3).
- **Say what will happen before it happens.** The examples open a visible Chrome window by default so the user can watch Claude work. Tell them a window will appear, and that each run calls the Anthropic API and is billed to their key.
- **Keep the user in the loop on the task.** Don't point the browser at sites that need the user's accounts, purchases, or personal data unless the user explicitly asks for it.

## Setup

### 1. Pick a language and a browser

Ask which language they prefer. If they have no preference, use the one their machine already has tooling for. Prefer TypeScript if both are present.

Ask where the browser should run:

- **Local Chrome:** the default. Requires Google Chrome, or another Chromium-based browser passed as `chromePath` / `chrome_path`. Firefox and Safari are not supported.
- **Browserbase:** a hosted browser, so no local Chrome is needed. Requires a Browserbase API key from https://www.browserbase.com.

### 2. Check prerequisites

Run the checks for the chosen language and fix what is missing, asking before installing anything system-wide.

```bash
# TypeScript
node --version     # needs v22.18.0 or later
pnpm --version     # if missing: corepack enable pnpm   (or npm install -g pnpm)

# Python
uv --version       # if missing: see https://docs.astral.sh/uv/getting-started/installation/
                   # uv installs Python 3.13 for the project itself if needed

# Local Chrome (skip for Browserbase)
ls "/Applications/Google Chrome.app" 2>/dev/null           # macOS
command -v google-chrome chromium chromium-browser         # Linux
```

If Chrome isn't installed and the user doesn't want to install it, offer Browserbase instead.

### 3. Install and add credentials

```bash
cd typescript && pnpm install       # or: cd python && uv sync
cp .env.example .env
```

Ask the user to open `.env` and set `ANTHROPIC_API_KEY`, plus `BROWSERBASE_API_KEY` if they chose Browserbase. Keys come from https://console.anthropic.com and https://www.browserbase.com. `.env` is gitignored in both directories.

Confirm that a key is set without printing it. This prints only a count; `1` means the key is present:

```bash
grep -c '^ANTHROPIC_API_KEY=..' .env
```

### 4. Switch to Browserbase (only if chosen)

Replace the `StagehandBrowser.launch(...)` call in the example with the Browserbase variant shown in that language's README ("Use Browserbase" section). Keep `allowedDomains` / `allowed_domains`. Everything else stays the same.

### 5. Run the example

```bash
pnpm example                                    # typescript/
uv run --env-file .env python example.py        # python/
```

Expected result: a Chrome window opens on `example.com`, Claude takes a screenshot or reads the page, and the printed messages end with Claude describing the page. The run takes well under a minute. The browser closes on its own when the run ends.

If it fails, check the troubleshooting table below before changing code.

## Try it out

Once the example passes, offer to run a task of the user's choosing. Change three things in the example file:

1. **The task:** the `content` of the user message.
2. **The allowed domains:** every site the task needs. An entry covers its subdomains, so `wikipedia.org` allows `en.wikipedia.org`. Navigation to any other site is refused, which keeps Claude on task.
3. **`max_tokens`:** raise it to 4096 or more for multi-step tasks, so Claude has room for a full final answer.

Starter tasks that need no login:

| Task | Allowed domains |
| --- | --- |
| "Go to Hacker News and list the top five stories with their points." | `news.ycombinator.com` |
| "Find the Wikipedia article on the Apollo 11 mission and tell me the landing date and crew." | `wikipedia.org` |
| "Search GitHub for the browserbase/stagehand repository and report its star count and latest release." | `github.com` |
| "Open the Python documentation and summarize what's new in the latest release." | `python.org` |

Let the user watch the window. Afterwards, point out what Claude did in the printed messages: the tool calls it made (navigate, read_page, find, click, type, screenshot) and its final answer.

To run Chrome without a window, for example on a server or in CI, set `headless: true` (TypeScript) or `headless=True` (Python).

## Use it in the user's own project

```bash
pnpm add @anthropic-ai/sdk stagehand-claude-sdk         # TypeScript
uv add anthropic stagehand-claude-sdk                   # Python (import as stagehand_claude_sdk)
```

The pattern is the same as the example:

- Create one `StagehandBrowser` per task.
- Pass the instance itself in `tools`.
- Let the tool runner loop.
- Close the browser in `finally` (TypeScript) or with `async with browser` (Python). The tool runner never closes it.

The Python driver is async, so use `AsyncAnthropic`.

Useful options for `StagehandBrowser.launch` (camelCase in TypeScript, snake_case in Python):

| Option | Purpose |
| --- | --- |
| `allowedDomains` / `blockedDomains` | Restrict where the browser may go. Blocked entries win. |
| `headless` | `false` to watch, `true` for servers. |
| `chromePath` | Use a specific Chromium-based browser. |
| `viewport` | Page size for screenshots and coordinates. |

`StagehandBrowser.connect({ cdpUrl })` drives a Chromium that is already running; `StagehandBrowser.browserbase({ apiKey })` creates a hosted session.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Authentication error or missing key | `ANTHROPIC_API_KEY` isn't set in `.env`. Re-check with the `grep -c` command above. |
| Model not found or not permitted | The account can't use the model in the example. Ask the user which Claude model they have access to and set it in the example. |
| Chrome doesn't launch | Install Google Chrome, pass `chromePath` / `chrome_path`, or switch to Browserbase. |
| `navigation refused` or blocked in the output | The site isn't in the allowed domains. Add it and rerun. |
| Package exports or attributes missing | The installed Anthropic SDK is older than the pinned version. Reinstall with `pnpm install` or `uv sync`. |
| Browser connection lost mid-run | Close the browser and create a new `StagehandBrowser`; a session isn't reused after its browser dies. |
| Downloads don't appear on Browserbase | Expected: downloads aren't available in Browserbase sessions. |

## Why Stagehand as the driver

Anthropic's browser toolset defines what Claude can do in a browser. A driver supplies the browser underneath. Anthropic ships reference drivers built directly on Playwright and on raw CDP. `StagehandBrowser` is the same toolset on Stagehand, Browserbase's open-source browser automation runtime, and it serves the full set of toolset tools in both TypeScript and Python.

### Where it does more than the CDP and Playwright drivers

- **The whole page is visible.** `read_page` and `find` are built from Chrome's accessibility tree across every frame. Content inside same-origin and cross-origin iframes and inside shadow DOM is listed and clickable. The CDP driver queries only the top document, so embedded checkout forms, payment widgets and web components are invisible to it.
- **Stable element references.** A reference names a specific node in a specific frame. If the page re-renders, the driver refuses the stale reference instead of clicking whatever now sits in that spot. After a click it also tells Claude if another element, such as a cookie banner, covered the target.
- **The page doesn't get stuck.**
  - JavaScript dialogs (`alert`, `confirm`, `prompt`) are handled and reported to Claude instead of freezing the page.
  - Popups and `target=_blank` links show up as new tabs, and downloads are reported.
  - After a click that loads a new page, the driver waits for the navigation to finish before Claude reads again.
- **Every toolset tool, not a subset.** The CDP example implements five tools. Stagehand covers typing, keys, hover, drag, scroll, form filling, tabs, screenshots and `find`, which most real tasks need.
- **One driver for local and hosted.** The same class launches local Chrome, attaches to a running Chromium, or opens a Browserbase session. On Browserbase, `file_upload` works too, because files travel to the remote browser rather than relying on a shared filesystem.
- **Domain restrictions enforced inside the browser.** Allowed and blocked domains apply to every HTTP(S) request and WebSocket handshake the page makes, not just top-level navigations. This is a guardrail, not complete network isolation.

### Performance and cost

Measured on HardBench, Browserbase's set of 38 tasks on live websites, with the same model, harness and step budget for each driver. Every result was graded by a verifier and then audited trajectory by trajectory for grading errors.

| Model | Driver | Tasks passed | Time per task | Cost per task |
| --- | --- | --- | --- | --- |
| Claude Sonnet 5 | Stagehand | **31 / 38 (81.6%)** | **7.9 min** | **$1.08** |
| Claude Sonnet 5 | CDP | 24 / 38 (63.2%) | 10.3 min | $2.85 |
| Claude Opus 5.5 | Stagehand | **29–34 / 38** (two runs) | **6.2–6.6 min** | **$0.69–0.76** |
| Claude Opus 5.5 | CDP | 30 / 38 (two runs) | 7.1–7.2 min | $2.05–2.92 |

- **Cost: 2.6–3.8× lower per task.** Claude needs fewer turns and fewer output tokens with Stagehand, and sends roughly a third of the data (2.9 MB vs 10.5 MB per task for Opus 5.5).
- **Speed: 8–24% faster on average**, from the same drop in turns.
- **Accuracy:** with Sonnet 5, Stagehand completed 7 more tasks. With Opus 5.5, the strongest model mostly compensated for the CDP driver's blind spots, and the two drivers were within run-to-run noise.

Against the Playwright reference driver, accuracy, speed and cost were within noise in our runs. There, the advantages are the capabilities above: iframes and shadow DOM, hosted browsers with uploads, and one driver from laptop to production.
