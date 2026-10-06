# Claude Toolset for Python

Run an async Claude browser task with the Anthropic SDK and the `stagehand-claude-sdk` Python package. This example opens `example.com` in headless Chrome and asks Claude for the page heading.

## Prerequisites

- Python 3.13 or later and uv, as required by this directory's `pyproject.toml`.
- Google Chrome for local execution, or a Browserbase API key for a hosted browser.
- An Anthropic API key with access to `claude-sonnet-5-5`, or another browser-toolset model you configure in the code.

## Install and run

Run these commands from this repository's `python` directory:

```bash
uv sync
cp .env.example .env
# Set ANTHROPIC_API_KEY in .env
uv run --env-file .env python example.py
```

The example prints the model's messages. Look for a response identifying the heading as **Example Domain**.

## How the example works

[example.py](example.py) imports the published package as `stagehand_claude_sdk`, registers the browser directly in `tools`, and closes it when the async context exits:

```python
import asyncio

from anthropic import AsyncAnthropic
from stagehand_claude_sdk import StagehandBrowser


async def main() -> None:
    browser = await StagehandBrowser.launch(
        headless=True,
        allowed_domains=["example.com", "iana.org"],
    )

    async with browser:
        runner = AsyncAnthropic().messages.tool_runner(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            tools=[browser],
            messages=[
                {
                    "role": "user",
                    "content": "Open example.com and tell me the page heading.",
                }
            ],
        )
        async for message in runner:
            print(message)


if __name__ == "__main__":
    asyncio.run(main())
```

Edit the model and task directly in `example.py`. Set `headless=False` to watch local Chrome, and update `allowed_domains` for your task's websites.

## Use Browserbase

Set `BROWSERBASE_API_KEY` in your `.env` file.

Add `import os` at the top of `example.py`, then replace the `StagehandBrowser.launch` call inside `main` with:

```python
browser = await StagehandBrowser.browserbase(
    api_key=os.environ["BROWSERBASE_API_KEY"],
    allowed_domains=["example.com", "iana.org"],
)
```

Keep the tool loop and `async with browser` block, then run `uv run --env-file .env python example.py` again. Browserbase creates the browser session, so you don't need local Chrome.

## Use in your own project

Add the dependencies to your uv project:

```bash
uv add 'anthropic>=1.12.0' stagehand-claude-sdk
```

The distribution name uses hyphens (`stagehand-claude-sdk`), but the Python import uses underscores (`stagehand_claude_sdk`).

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Missing API key | Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY`. |
| Model access error | Set a browser-toolset model available to your account directly in `example.py`. |
| Chrome doesn't launch | Install Google Chrome or pass `chrome_path` to `launch`. |
| Navigation is blocked | Check `allowed_domains` and `blocked_domains`. |
| Missing module or exports | Run `uv sync` and check that the installed package releases provide the browser toolset. |

See the [shared limitations](../README.md#limitations) for domain filtering and Browserbase downloads, or return to the [repository overview](../README.md).
