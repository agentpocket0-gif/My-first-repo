#!/usr/bin/env python3
"""Generate a complete HTML5 game (2D or 3D) from an idea using the DeepSeek API.

Usage:
    python3 scripts/generate_game.py --idea-file /tmp/idea.txt --out game/index.html \
        --name "My Game" --engine three --three-file /tmp/three.min.js

If DEEPSEEK_API_KEY is missing or generation fails, the bundled game stays in place.
"""
import argparse
import json
import os
import re
import urllib.request

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

COMMON_RULES = (
    "You are an expert HTML5 game developer and game designer. "
    "You output ONLY a complete, self-contained HTML5 game in a single file. "
    "Hard rules: the file must run fully offline; no external URLs, CDNs, fonts, images or network calls; "
    "support both mobile touch/drag controls and keyboard arrows; "
    "UI text in Hindi with English hints; include a start screen, score display and game-over/retry; "
    "make it polished, fun and immediately playable. "
    "Output raw HTML only - no markdown fences, no explanations."
)


def system_prompt(engine):
    if engine == "three":
        return (
            COMMON_RULES
            + " This is a 3D game. Use the global THREE object (Three.js r128) - it is ALREADY INCLUDED "
            "in the page by the build system, so never add <script src=...> or import statements. "
            "Write plain JavaScript using THREE.Scene, THREE.PerspectiveCamera, THREE.WebGLRenderer, and simple "
            "geometries (BoxGeometry, CylinderGeometry, SphereGeometry) with MeshLambertMaterial, plus "
            "AmbientLight and DirectionalLight. Use scene.fog for depth. OrbitControls are NOT available. "
            "Make the 3D feel real: a ground plane, moving objects toward/around the player, camera shake or "
            "tilt on movement, and a clear goal."
        )
    return (
        COMMON_RULES
        + " This is a 2D game. Draw all graphics with the canvas 2D API or inline SVG."
    )


def validate(html: str, engine: str) -> str:
    errors = []
    low = html.lower()
    if "<html" not in low and "<!doctype" not in low:
        errors.append("missing <html> document skeleton")
    if "<canvas" not in low:
        errors.append("no <canvas> element")
    if "<script" not in low:
        errors.append("no <script> logic")
    if "http://" in low or "https://" in low:
        errors.append("contains external URLs (must run offline)")
    if engine == "three":
        if "THREE." not in html:
            errors.append("does not use the THREE library")
        if "renderer" not in low:
            errors.append("no renderer setup")
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


def embed_three(html: str, three_file: str) -> str:
    """Inject the Three.js source directly into the page so the game runs offline."""
    with open(three_file, encoding="utf-8") as f:
        three_src = f.read()
    inject = "<script>\n" + three_src + "\n</script>\n"
    m = re.search(r"<head[^>]*>", html, re.I)
    if m:
        return html[: m.end()] + "\n" + inject + html[m.end():]
    return inject + html


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--idea-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", default="My Game")
    ap.add_argument("--engine", choices=["canvas2d", "three"], default="canvas2d")
    ap.add_argument("--three-file", default=None,
                    help="Path to three.min.js; required for --engine three")
    args = ap.parse_args()

    if args.engine == "three" and not args.three_file:
        print("ERROR: --engine three needs --three-file")
        return

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
        {"role": "system", "content": system_prompt(args.engine)},
        {"role": "user", "content": "Game idea: " + idea + "\nGame name: " + args.name
         + "\nBuild the complete game now as a single HTML file."},
    ]

    html = None
    for attempt in range(2):
        print("Calling DeepSeek API (attempt %d, engine=%s)..." % (attempt + 1, args.engine))
        raw = call_api(key, messages, 8192)
        candidate = strip_fences(raw)
        errors = validate(candidate, args.engine)
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

    if args.engine == "three":
        html = embed_three(html, args.three_file)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Game written to %s (%d bytes)" % (args.out, len(html)))


if __name__ == "__main__":
    main()
