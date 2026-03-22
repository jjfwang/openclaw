#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://api.manus.ai/v1"
DEFAULT_ENV_FILE = "/home/pi/Repos/ideation/manus-orchestrator/.env"


def load_env_file(path: str) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def resolve_config(env_file: str | None, base_url_arg: str | None) -> tuple[str, str]:
    if env_file:
        load_env_file(env_file)
    elif Path(DEFAULT_ENV_FILE).exists():
        load_env_file(DEFAULT_ENV_FILE)
    elif Path(LEGACY_ENV_FILE).exists():
        load_env_file(LEGACY_ENV_FILE)
    api_key = os.getenv("MANUS_API_KEY") or os.getenv("ORCH_MANUS_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing Manus API key. Set MANUS_API_KEY or ORCH_MANUS_API_KEY, "
            "or pass --env-file pointing to a .env file that contains one."
        )
    base_url = (
        base_url_arg
        or os.getenv("MANUS_API_BASE")
        or os.getenv("ORCH_MANUS_API_BASE")
        or DEFAULT_BASE_URL
    ).rstrip("/")
    return api_key, base_url


def request_json(method: str, url: str, api_key: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(url, method=method)
    req.add_header("API_KEY", api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req, data=data, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} from Manus API: {body[:500]}") from exc
    except URLError as exc:
        raise SystemExit(f"Failed to reach Manus API: {exc}") from exc


def cmd_create(args: argparse.Namespace) -> int:
    api_key, base_url = resolve_config(args.env_file, args.base_url)
    prompt = args.prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text()
    if not prompt:
        raise SystemExit("Provide --prompt or --prompt-file")

    payload: dict[str, Any] = {
        "prompt": prompt,
        "agentProfile": args.agent_profile,
    }
    if args.project_id:
        payload["projectId"] = args.project_id
    if args.connectors:
        payload["connectors"] = args.connectors
    if args.continue_task_id:
        payload["taskId"] = args.continue_task_id

    result = request_json("POST", f"{base_url}/tasks", api_key, payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    api_key, base_url = resolve_config(args.env_file, args.base_url)
    result = request_json("GET", f"{base_url}/tasks/{args.task_id}", api_key)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_wait(args: argparse.Namespace) -> int:
    api_key, base_url = resolve_config(args.env_file, args.base_url)
    start = time.monotonic()
    last_status = None
    while True:
        result = request_json("GET", f"{base_url}/tasks/{args.task_id}", api_key)
        status = result.get("status", "unknown")
        if status != last_status:
            print(f"status={status}", file=sys.stderr)
            last_status = status
        if status in {"completed", "failed", "cancelled"}:
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if status == "completed" else 1
        if time.monotonic() - start > args.timeout:
            raise SystemExit(f"Timed out after {args.timeout}s waiting for task {args.task_id}")
        time.sleep(args.poll_interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create, inspect, and wait on Manus tasks.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Optional .env file to source for MANUS_API_KEY / MANUS_API_BASE (falls back to legacy ideation env if omitted and needed)")
    parser.add_argument("--base-url", help="Override Manus API base URL")

    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a Manus task")
    create.add_argument("--prompt", help="Prompt text for the Manus task")
    create.add_argument("--prompt-file", help="Read prompt text from a file")
    create.add_argument("--agent-profile", default="manus-1.6-max", help="Manus agent profile")
    create.add_argument("--project-id", help="Optional Manus project id")
    create.add_argument("--continue-task-id", help="Continue an existing Manus task thread")
    create.add_argument("--connectors", nargs="*", help="Optional connector ids")
    create.set_defaults(func=cmd_create)

    get_task = sub.add_parser("get", help="Fetch a Manus task")
    get_task.add_argument("task_id")
    get_task.set_defaults(func=cmd_get)

    wait = sub.add_parser("wait", help="Poll until a Manus task finishes")
    wait.add_argument("task_id")
    wait.add_argument("--poll-interval", type=int, default=10)
    wait.add_argument("--timeout", type=int, default=3600)
    wait.set_defaults(func=cmd_wait)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
