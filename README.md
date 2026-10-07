# Claude Toolset

Give Claude a browser through the Anthropic SDK. `StagehandBrowser` uses [Stagehand](https://stagehand.dev) to handle navigation, screenshots, and page interactions while the Anthropic SDK manages the model's tool loop.

This repository contains TypeScript and Python examples that import the published `stagehand-claude-sdk` packages.

> [!WARNING]
> Demo and reference code only. Browserbase does not claim that any recipe, integration, target, data source, vendor, or workflow in this repository has been vetted, approved, secured, or validated for production use. Independently review the code and obtain all required authorization before running it. You are responsible for compliance, site terms, privacy, security, costs, and outcomes. Use at your own risk.

## Choose your quickstart

| Language | Guide | Requirements | Package |
| --- | --- | --- | --- |
| TypeScript | [TypeScript quickstart](typescript/README.md) | Node.js 22.18+ and pnpm | [npm](https://www.npmjs.com/package/stagehand-claude-sdk) |
| Python | [Python quickstart](python/README.md) | Python 3.13+ and uv | [PyPI](https://pypi.org/project/stagehand-claude-sdk/) |

Both examples open `example.com`, ask Claude for the page heading, and print the model's messages. You'll need an Anthropic API key and access to the model defined in the example.

```bash
git clone https://github.com/browserbase/claude-cua-toolset.git
cd claude-cua-toolset
```

Open either language guide for installation, credentials, and run commands. If you've already cloned the repository, start in the corresponding language directory.

## Choose a browser

- **Local Chrome:** Run the examples as written. They launch headless Chrome, so install Google Chrome first.
- **Browserbase:** Run without local Chrome by replacing `StagehandBrowser.launch` with `StagehandBrowser.browserbase` and providing a Browserbase API key. Both language guides include the replacement code.

Keep the same browser instance throughout the tool loop. Close it when the task finishes or fails; the Anthropic tool runner doesn't close it for you.

## Adapt the example

Change the task in `messages` and set the model directly in `example.ts` or `example.py`. Update the allowed domains to include the sites your task needs.

| Setting | TypeScript | Python |
| --- | --- | --- |
| Browser toolset import | `stagehand-claude-sdk` | `stagehand_claude_sdk` |
| Allowed domains | `allowedDomains` | `allowed_domains` |
| Blocked domains | `blockedDomains` | `blocked_domains` |
| Chrome executable | `chromePath` | `chrome_path` |
| Cleanup | `await browser.close()` in `finally` | `async with browser` |

## Limitations

- Domain lists restrict HTTP and HTTPS requests. A domain entry includes its subdomains, and blocked entries take precedence.
- Domain restrictions don't cover WebSocket handshakes. Don't treat the lists as complete network isolation.
- Local browsers must be Chromium-based. Firefox and WebKit aren't supported.
- Downloads aren't supported in Browserbase sessions.
- If the browser connection is lost, close the toolset and create a new instance.

## Examples

- [TypeScript browser task](typescript/example.ts)
- [Python browser task](python/example.py)

## License

[MIT](LICENSE)
