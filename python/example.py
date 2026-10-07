import asyncio

from anthropic import AsyncAnthropic
from stagehand_claude_sdk import StagehandBrowser


async def main() -> None:
    browser = await StagehandBrowser.launch(
        headless=False,
        allowed_domains=["example.com", "iana.org"],
    )
    async with browser:
        runner = AsyncAnthropic().messages.tool_runner(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            tools=[browser],
            messages=[{"role": "user", "content": "Open example.com and tell me the page heading."}],
        )
        async for message in runner:
            print(message)


if __name__ == "__main__":
    asyncio.run(main())
