from __future__ import annotations

import argparse
from pathlib import Path

from work_automation_pipeline.pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_pipeline(args.input, args.output)
        print(
            "Generated report "
            f"at {result.report_path} "
            f"({result.estimated_saved_minutes_per_week} min/week estimated savings)"
        )
        return 0

    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="work-auto",
        description="Find and package repetitive workplace tasks for GPT/Codex automation.",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Generate an automation report")
    run_parser.add_argument("--input", required=True, type=Path, help="CSV task inventory")
    run_parser.add_argument("--output", required=True, type=Path, help="Markdown report path")

    return parser


if __name__ == "__main__":
    raise SystemExit(main())
