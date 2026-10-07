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
    messages: [{ role: "user", content: "Open example.com and tell me the page heading." }],
  });
  for await (const message of runner) console.log(JSON.stringify(message, null, 2));
} finally {
  await browser.close();
}
