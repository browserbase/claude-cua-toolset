# Claude Toolset for TypeScript

Run a Claude browser task with the Anthropic SDK and the `stagehand-claude-sdk` npm package. This example opens `example.com` in a visible Chrome window and asks Claude for the page heading.

## Prerequisites

- Node.js 22.18 or later and pnpm.
- Google Chrome for local execution, or a Browserbase API key for a hosted browser.
- An Anthropic API key with access to `claude-sonnet-5-5`, or another browser-toolset model you configure in the code.

## Install and run

Run these commands from this repository's `typescript` directory:

```bash
pnpm install
cp .env.example .env
# Set ANTHROPIC_API_KEY in .env
pnpm example
```

The example prints the model's messages. Look for a response identifying the heading as **Example Domain**.

## How the example works

[example.ts](example.ts) imports the published package, registers the browser directly in `tools`, and closes it in `finally`:

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { StagehandBrowser } from "stagehand-claude-sdk";

const browser = await StagehandBrowser.launch({
  headless: false,
  allowedDomains: ["example.com", "iana.org"],
});

try {
  const runner = new Anthropic().messages.toolRunner({
    model: "claude-sonnet-5-5",
    max_tokens: 1024,
    tools: [browser],
    messages: [
      { role: "user", content: "Open example.com and tell me the page heading." },
    ],
  });

  for await (const message of runner) {
    console.log(JSON.stringify(message, null, 2));
  }
} finally {
  await browser.close();
}
```

Edit the model and task directly in `example.ts`. Set `headless: true` to run without a visible Chrome window, and update `allowedDomains` for your task's websites.

## Use Browserbase

Set `BROWSERBASE_API_KEY` in your `.env` file.

Replace the `StagehandBrowser.launch` call in `example.ts` with:

```typescript
const apiKey = process.env.BROWSERBASE_API_KEY;
if (!apiKey) throw new Error("Set BROWSERBASE_API_KEY before running this example.");

const browser = await StagehandBrowser.browserbase({
  apiKey,
  allowedDomains: ["example.com", "iana.org"],
});
```

Keep the tool loop and `finally` block, then run `pnpm example` again. Browserbase creates the browser session, so you don't need local Chrome.

## Use in your own project

Install the packages in your TypeScript project:

```bash
pnpm add @anthropic-ai/sdk@0.132.0 stagehand-claude-sdk
```

Use the imports and tool loop above with an ESM-compatible TypeScript runner. This repository uses `tsx` through its `example` script.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Missing API key | Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY`. |
| Model access error | Set a browser-toolset model available to your account directly in `example.ts`. |
| Chrome doesn't launch | Install Google Chrome or pass `chromePath` to `launch`. |
| Navigation is blocked | Check `allowedDomains` and `blockedDomains`. |
| Missing package exports | Check that the installed `stagehand-claude-sdk` and Anthropic SDK releases provide the browser toolset. |

See the [shared limitations](../README.md#limitations) for domain filtering and Browserbase downloads, or return to the [repository overview](../README.md).
