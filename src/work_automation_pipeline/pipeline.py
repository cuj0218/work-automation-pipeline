from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = {"task", "team", "minutes", "frequency", "automation_hint"}
FREQUENCY_MULTIPLIERS = {
    "daily": 5,
    "weekly": 1,
    "monthly": 0.25,
}


@dataclass(frozen=True)
class TaskRecord:
    task: str
    team: str
    minutes: int
    frequency: str
    automation_hint: str

    @property
    def weekly_minutes(self) -> int:
        multiplier = FREQUENCY_MULTIPLIERS.get(self.frequency.lower(), 1)
        return int(self.minutes * multiplier)


@dataclass(frozen=True)
class PipelineResult:
    total_tasks: int
    total_manual_minutes_per_week: int
    estimated_saved_minutes_per_week: int
    highest_impact_task: TaskRecord
    report_path: Path


def run_pipeline(input_path: str | Path, output_path: str | Path) -> PipelineResult:
    input_file = Path(input_path)
    output_file = Path(output_path)
    tasks = load_tasks(input_file)
    if not tasks:
        raise ValueError("Input file must contain at least one task")

    total_minutes = sum(task.weekly_minutes for task in tasks)
    saved_minutes = int(total_minutes * 0.7)
    highest_impact_task = max(tasks, key=lambda task: task.weekly_minutes)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        render_report(tasks, total_minutes, saved_minutes),
        encoding="utf-8",
    )

    return PipelineResult(
        total_tasks=len(tasks),
        total_manual_minutes_per_week=total_minutes,
        estimated_saved_minutes_per_week=saved_minutes,
        highest_impact_task=highest_impact_task,
        report_path=output_file,
    )


def load_tasks(input_file: Path) -> list[TaskRecord]:
    with input_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - fieldnames
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns: {missing}")

        return [
            TaskRecord(
                task=row["task"].strip(),
                team=row["team"].strip(),
                minutes=int(row["minutes"]),
                frequency=row["frequency"].strip().lower(),
                automation_hint=row["automation_hint"].strip(),
            )
            for row in reader
        ]


def render_report(
    tasks: list[TaskRecord],
    total_manual_minutes_per_week: int,
    estimated_saved_minutes_per_week: int,
) -> str:
    lines = [
        "# Work Automation Pipeline Report",
        "",
        "## Summary",
        "",
        f"- Total tasks: {len(tasks)}",
        f"- Manual workload: {total_manual_minutes_per_week} minutes/week",
        f"- Estimated saved time: {estimated_saved_minutes_per_week} minutes/week",
        "",
        "## Automation Candidates",
        "",
        "| Task | Team | Frequency | Weekly minutes | Automation hint |",
        "| --- | --- | --- | ---: | --- |",
    ]

    for task in sorted(tasks, key=lambda item: item.weekly_minutes, reverse=True):
        lines.append(
            "| "
            f"{task.task} | "
            f"{task.team} | "
            f"{task.frequency} | "
            f"{task.weekly_minutes} | "
            f"{task.automation_hint} |"
        )

    lines.extend(
        [
            "",
            "## GPT/Codex Prompt Starter",
            "",
            "Use the table above to generate a scoped automation plan. For each task, identify inputs, outputs, failure cases, and the smallest script or agent workflow that can remove manual work.",
            "",
        ]
    )
    return "\n".join(lines)
