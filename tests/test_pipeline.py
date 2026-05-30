from pathlib import Path

from work_automation_pipeline.pipeline import run_pipeline


def test_pipeline_groups_tasks_and_writes_markdown_report(tmp_path):
    input_file = tmp_path / "tasks.csv"
    output_file = tmp_path / "report.md"
    input_file.write_text(
        "task,team,minutes,frequency,automation_hint\n"
        "Invoice check,Finance,30,daily,Compare spreadsheet rows\n"
        "Lead cleanup,Sales,45,weekly,Normalize CRM fields\n",
        encoding="utf-8",
    )

    result = run_pipeline(input_file, output_file)

    assert result.total_tasks == 2
    assert result.total_manual_minutes_per_week == 195
    assert result.estimated_saved_minutes_per_week == 136
    assert result.highest_impact_task.task == "Invoice check"
    assert output_file.exists()
    report = output_file.read_text(encoding="utf-8")
    assert "# Work Automation Pipeline Report" in report
    assert "Invoice check" in report
    assert "Lead cleanup" in report


def test_pipeline_rejects_missing_required_columns(tmp_path):
    input_file = tmp_path / "bad.csv"
    output_file = tmp_path / "report.md"
    input_file.write_text("task,minutes\nInvoice check,30\n", encoding="utf-8")

    try:
        run_pipeline(input_file, output_file)
    except ValueError as exc:
        assert "Missing required columns" in str(exc)
        assert "team" in str(exc)
    else:
        raise AssertionError("run_pipeline should reject incomplete CSV input")
