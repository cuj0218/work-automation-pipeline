from pathlib import Path

from work_automation_pipeline.cli import main


def test_cli_generates_report_from_arguments(tmp_path, capsys):
    input_file = tmp_path / "tasks.csv"
    output_file = tmp_path / "report.md"
    input_file.write_text(
        "task,team,minutes,frequency,automation_hint\n"
        "Daily status summary,Operations,20,daily,Summarize ticket comments\n",
        encoding="utf-8",
    )

    exit_code = main(["run", "--input", str(input_file), "--output", str(output_file)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Generated report" in captured.out
    assert output_file.exists()
