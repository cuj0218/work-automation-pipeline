# Work Automation Pipeline

GPT와 Codex를 활용해 반복적인 운영 업무를 자동화하기 위한 오픈소스 파이프라인 템플릿입니다.

이 프로젝트는 직장인이 매일 처리하는 정산, 리포트, CRM 정리, 티켓 요약 같은 반복 업무를 CSV로 정리한 뒤 자동화 우선순위와 GPT/Codex 실행 프롬프트 초안을 Markdown 리포트로 만들어줍니다. 실제 업무 환경에서 수작업 처리 시간을 70% 이상 줄이는 것을 목표로 설계했습니다.

## Why

많은 팀은 자동화할 수 있는 업무를 알고 있어도 어디서부터 시작할지 정리하지 못해 시간을 잃습니다. 이 저장소는 업무 목록을 구조화하고, 자동화 후보를 계산하고, 바로 Codex나 GPT에게 넘길 수 있는 구현 브리프를 생성하는 최소 파이프라인을 제공합니다.

## Features

- CSV 기반 반복 업무 인벤토리 입력
- 업무별 주간 수작업 시간 계산
- 70% 절감 기준의 예상 절약 시간 산출
- 자동화 우선순위 Markdown 리포트 생성
- GPT/Codex 자동화 프롬프트 스타터 포함
- 회사와 업종별로 바꿔 쓰기 쉬운 예시 템플릿 제공

## Quick Start

```bash
git clone https://github.com/YOUR_NAME/work-automation-pipeline.git
cd work-automation-pipeline
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
work-auto run --input examples/tasks.csv --output output/report.md
```

결과 파일은 `output/report.md`에 생성됩니다.

## Input Format

`examples/tasks.csv`처럼 아래 컬럼을 준비합니다.

| Column | Description |
| --- | --- |
| `task` | 반복 업무 이름 |
| `team` | 담당 팀 |
| `minutes` | 1회 처리 시간 |
| `frequency` | `daily`, `weekly`, `monthly` 중 하나 |
| `automation_hint` | 자동화 아이디어 |

## Example

```csv
task,team,minutes,frequency,automation_hint
Invoice check,Finance,30,daily,Compare spreadsheet rows
Lead cleanup,Sales,45,weekly,Normalize CRM fields
```

실행:

```bash
work-auto run --input examples/tasks.csv --output output/report.md
```

요약 결과:

```text
Manual workload: 380 minutes/week
Estimated saved time: 266 minutes/week
```

## Project Fit

이 프로젝트는 실무에서 검증된 반복 업무 자동화 방식을 공개 템플릿으로 전환해 더 많은 팀이 재사용할 수 있게 만드는 것을 목표로 합니다. API 크레딧은 업무 유형별 템플릿 확장, GPT 기반 분류/요약 단계 추가, 실제 사용자 사례 문서화에 활용할 수 있습니다.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest
```

현재 테스트 의존성은 `pytest`입니다.

```bash
python -m pip install pytest
python -m pytest
```

## Roadmap

- JSON 입력 지원
- 팀별 자동화 템플릿 추가
- OpenAI API를 활용한 업무 분류 단계
- GitHub Actions 기반 테스트 자동화
- 사용자 사례와 절감 시간 벤치마크 문서화

## Contributing

이슈와 PR을 환영합니다. 반복 업무 사례, 업종별 템플릿, 문서 개선 모두 기여로 인정합니다.

## License

MIT License
