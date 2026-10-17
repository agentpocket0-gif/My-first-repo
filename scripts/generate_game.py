#!/usr/bin/env python3
"""Generate a complete HTML5 game from an idea using the DeepSeek API.

Usage:
    python3 scripts/generate_game.py --idea-file /tmp/idea.txt --out game/index.html --name "My Game"

If DEEPSEEK_API_KEY is missing or generation fails, the bundled game stays in place.
"""
import argparse
import json
import os
import re
import urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

SYSTEM_PROMPT = (
    "You are an expert HTML5 game developer and game designer. "
    "You output ONLY a complete, self-contained HTML5 game in a single file. "
    "Hard rules: the file must run fully offline; no external URLs, CDNs, fonts, images or network calls; "
    "draw all graphics with canvas, CSS or inline SVG; support both mobile touch/drag controls and keyboard arrows; "
    "UI text in Hindi with English hints; include a start screen, score display and game-over/retry; "
    "make it polished, fun and immediately playable; keep total file size reasonable. "
    "Output raw HTML only - no markdown fences, no explanations."
)


def validate(html: str) -> str:
    errors = []
    low = html.lower()
    if "<html" not in low and "<!doctype" not in low:
        errors.append("missing <html> document skeleton")
    if "<canvas" not in low and "<svg" not in low:
        errors.append("no canvas/svg graphics")
    if "<script" not in low:
        errors.append("no <script> logic")
    if "http://" in low or "https://" in low:
        errors.append("contains external URLs (must run offline)")
    return "; ".join(errors)


def call_api(key: str, messages: list, max_tokens: int) -> str:
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.8,
    }).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.load(resp)
    return data["choices"][0]["message"]["content"]


def strip_fences(text: str) -> str:
    m = re.search(r"```(?:html)?\s*(.*?)```", text, re.S)
    return m.group(1).strip() if m else text.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--idea-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", default="My Game")
    args = ap.parse_args()

    with open(args.idea_file, encoding="utf-8") as f:
        idea = f.read().strip()
    if not idea:
        print("No idea provided; keeping bundled game.")
        return

    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        print("DEEPSEEK_API_KEY not set; keeping bundled game.")
        return

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Game idea: " + idea + "
Game name: " + args.name
         + "
Build the complete game now as a single HTML file."},
    ]

    html = None
    for attempt in range(2):
        print("Calling DeepSeek API (attempt %d)..." % (attempt + 1))
        raw = call_api(key, messages, 8192)
        candidate = strip_fences(raw)
        errors = validate(candidate)
        if not errors:
            html = candidate
            break
        print("Validation failed: %s" % errors)
        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": "That output was invalid: " + errors
                         + ". Output the corrected, complete single HTML file again. Raw HTML only."})

    if html is None:
        print("API output invalid after retries; keeping bundled game.")
        return

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Game written to %s (%d bytes)" % (args.out, len(html)))


if __name__ == "__main__":
    main()
