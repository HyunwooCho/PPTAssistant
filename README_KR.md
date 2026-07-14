# PPT Assistant

<p align="right">
  <a href="README.md">English</a> |
  <strong>한국어</strong>
</p>

파워포인트에서 맞춤법 빨간 밑줄 제거, 회사 스타일로 포맷을 통일하는 유틸리티

**저자:** tenace@etri.re.kr
**현재 개발 버전:** 3.0.0-alpha
**지원 파이썬 버전:** 3.12+

---

## 프로젝트 개요

PPT Assistant는 파워포인트 편집시 아래와 같이 반복적이고 귀찮은 작업을 자동화하는 것을 목표로 한다.

* ChatGPT 답변 등 웹에서 긁어온 내용을 PPT에 붙일 경우 한국어에 대해 맞춤법이 틀리다며 빨간 밑줄이 그어지는 것을 제거
* 템플릿에서 특성을 추출하고 그에 맞추어 PPT 포맷 변경
 - 폰트 통일
 - 테이블 형식 통일
 - 배경 그림 추출 및 최적화 적용(이미지 크기 압축)
* 여러 PPT 파일에 대해 처리
* PDF 파일로 출력

이 프로젝트는 `.pptx` 파일의 내부 XML 구조를 수정하여 위의 작업을 수행한다.

---

## 현재 구현된 기능들

* 변경하길 원하는 PPTX 파일을 선택하거나 드래그-앤-드랍 할 수 있는 GUI
* 여러 파일에 대해 동시 처리 지원
* 맞춤법 메터데이터 제거 (빨간 밑줄 제거)
* 한국어 맞춤법으로 설정
* 폰트 통일
* 발표자 노트 제거 지원(사용자 체크시)
* 처리 로그 제공
* 처리 진행율 제공
* 빌트인 ETRI 스타일 일부(폰트) 제공
* 커스텀 스타일 추출 프레임워크 (아직은 껍데기만 있음)

---

## 앞으로 구현할 기능들

* 빌트인 ETRI 스타일 완성(폰트, 테이블, 레이아웃, 배경 이미지)
* 커스텀 스타일 추출 기능 구현
 - 배경 이미지 추출 및 최적화(압축)
 - 레이아웃 형식 추출
 - 테이블 형식 추출
 - 사용하지 않는 슬라이드 마스터 제거
 - 커스텀 스타일에 테이블 형식 없을 경우 기본 테이블 형식 제공
* PDF 출력
* PPT에 플러그인 시스템 구현
* AI 슬라이드 검토 기능

---

## 개발 환경

| Item                  | Requirement              |
| --------------------- | ------------------------ |
| Operating system      | Windows 10 or Windows 11 |
| Python                | 3.12 or later            |
| IDE                   | Visual Studio Code       |
| GUI framework         | PySide6                  |
| PowerPoint processing | python-pptx, lxml        |
| Image processing      | Pillow                   |
| Testing               | pytest                   |
| Formatting            | Black                    |
| Linting               | Ruff                     |
| Packaging             | PyInstaller              |

---

## 코딩 환경 설정

(전제) Windows용 git, Visual Studio Code, Python이 설치되어 있다고 가정

Visual Studio Code에서 본 프로젝트 오픈

```cmd
cd C:\Projects\PPTAssistant
```

Visual Studio Code의 Terminal(cmd 추천)에서 가상 환경 생성

```cmd
python -m venv .venv
```

가상 환경 활성화

```cmd
.venv\Scripts\activate.bat
```

터미널 프롬프트가 아래와 같이 변경되는 지 확인

```text
(.venv) C:\Projects\PPTAssistant>
```

pip 업그레이드

```cmd
python -m pip install --upgrade pip
```

의존성 설치

```cmd
pip install -e ".[dev]"
```

---

## Visual Stiod Code 설정

일관되고 지속적인 개발을 위해 본 프로젝트는 `.vscode` 디렉토리 활용

```text
.vscode/
├── settings.json
├── launch.json
├── tasks.json
└── extensions.json
```

`.venv` Python 인터프리터를 Visual Studio Code의 파이썬 인터프리터로 설정

Visual Studio Code에서 아래와 같은 단축키 이용

```text
Ctrl + Shift + P
```

상단에 나오는 검색 창에 아래와 같이 기입하여 선택

```text
Python: Select Interpreter
```

그러면 나오는 여러 가지 옵션 중에 아래를 선택

```text
.venv\Scripts\python.exe
```
### F5를 눌러서 실행(run)

이제 코드를 수정하고 실행하고 싶으면 **F5**만 누르면 바로 확인 가능

---

## EXE 실행 파일 빌드

최종 빌드의 목표 출력은 아래와 같이 단독으로 수행가능한 윈도우즈 실행 파일(.exe)이다.

```text
dist\PPTAssistant.exe
```

이를 위한 최종 빌드 과정은 다음을 이용한다.

```cmd
python build_release.py
```

이 릴리즈 스크립트는 아래와 같은 일을 담당한다.

* Python 환경 검증
* 빌드 의존성 설치
* test 실행
* Ruff 실행
* Black check 실행
* PyInstaller 실행
* Standalone executable(.exe) 생성
* 릴리즈 패키지 생성

`build_release.py`로 배포하기 전까지 개발은 다음을 이용하는 것을 권장한다.
(**F5**를 누르는 것과 같음)

```cmd
python -m pptassistant
```

---

## 단위 시험

추가 기능 구현 후 CI/CD를 위해 반드시 test\ 디렉토리에 해당 기능 시험 파일 구현

test\ 디렉토리 내의 모든 테스트는 아래 명령어로 실행

```cmd
pytest
```

만약 로그를 상세히 보고 싶을 경우는 옵션을 추가하여 실행

```cmd
pytest -v
```

특정 시험 파일만 동작 여부를 확인하고 싶을 경우는 직접 파일 명까지 기입하여 실행

```cmd
pytest tests\test_proofing.py
```

## 코드 품질 관리

Ruff를 이용한 코드의 Link 확인

```cmd
ruff check .
```

Ruff 이슈가 발생하면 자동 고침을 하려면 아래 옵션을 추가하여 실행

```cmd
ruff check . --fix
```

Black을 이용한 코드의 포맷 통일

```cmd
black .
```

만약 수정 없이 포맷 이슈만 체크하고 싶을 때는 아래 옵션을 추가하여 실행

```cmd
black --check .
```

---

## 저장소 레이아웃

```text
PPTAssistant/
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT.md
│   └── ROADMAP.md
│
├── src/
│   └── pptassistant/
│       ├── gui/
│       ├── engine/
│       │   ├── cleanup/
│       │   ├── proofing/
│       │   ├── style/
│       │   ├── table/
│       │   └── optimizer/
│       ├── profiles/
│       ├── resources/
│       ├── main.py
│       └── __main__.py
│
├── tests/
├── build_release.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── LICENSE
```

---

# 본 프로젝트의 개발 원칙

1. 원본 파워포인트 파일을 덮어쓰지 말 것
2. 항상 별도의 출력 파일을 생성할 것
3. 가능한 한 사용자 콘텐츠는 보존할 것
4. 파워포인트 COM 자동화보다는 PPTX XML 처리를 할 것
5. MS 오피스 없이 핵심 프로세스가 동작할 것
6. 처리 결과는 GUI 및 CLI 모두에서 재사용 가능할 것
7. 시험 항목은 모듈화하여 독립적으로 테스트할 수 있을 것
8. 모든 주요 프로세스 동작은 로그를 남길 것
9. 미지원 파워포인트 구조에 대해서는 안전한 실패를 지원할 것
10. 스타일 프로파일은 프로세스 로직과 분리시킬 것

---


# 코딩 규칙

## Python

본 프로젝트는 다음과 같은 파이썬 코딩 규칙을 따른다.

* Python 3.12+
* UTF-8 포맷
* 함수/메소드에 타입 힌트 기입
* 모듈, 클래스, 함수, 메소드에 Docstring 기입
* Black 포맷
* Ruff 린트
* 각 기능을 테스트할 수 있도록 작고 독립적인 시험 모듈 구현
* 명시적인 예외 처리
* 경로는 `pathlib.Path` 위주로 작성
* 구조체는 되도록 Dataclass로 구현

예시:

```python
from pathlib import Path

from pptassistant.profiles.models import StyleProfile


def extract_style(template: Path) -> StyleProfile:
    """Extract a reusable style profile from a PowerPoint template."""
```

---

# Git 규칙

Commit 메시지는 다음과 같은 간략화된 포맷을 따른다.

```text
feat: Add style extractor

fix: Remove proofing metadata from grouped shapes

refactor: Improve PPTX XML parser

docs: Update README

test: Add proofing-engine tests

style: Apply Black formatting

chore: Update dependencies

build: Add PyInstaller release script

ci: Add GitHub Actions workflow
```

## Commit Types

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `refactor` | Internal code restructuring    |
| `docs`     | Documentation changes          |
| `test`     | Test additions or changes      |
| `style`    | Formatting-only changes        |
| `chore`    | Maintenance work               |
| `build`    | Build-system changes           |
| `ci`       | Continuous-integration changes |

---

# 브랜치 만드는 원칙

주 브랜치:

```text
main
develop
```

기능 구현 브랜치:

```text
feature/style-engine
feature/table-engine
feature/theme-extractor
feature/image-optimizer
feature/pdf-export
```

버그 수정 브랜치:

```text
bugfix/proofing
bugfix/gui
bugfix/template-parser
```

릴리즈 브랜치

```text
release/v3.0
release/v3.1
```

## 브랜치 역할

* `main`: 안정적으로 릴리즈 가능한 버전
* `develop`: 현재 개발 중인 하부 브랜치를 모두 집적한 브랜치
* `feature/*`: 새로운 기능 구현 브랜치
* `bugfix/*`: 버그 수정 브랜치
* `release/*`: 릴리즈 준비 브랜치

---

# Github 프로젝트 관리

Kanban-style Github 프로젝트 보드 사용

```text
To Do
Doing
Review
Done
```

초기 제안 이슈들:

```text
ChatGPT Cleanup
Remove Proofing
ETRI Style
Theme Extractor
Table Engine
Image Optimizer
PDF Export
Plugin System
AI Slide Reviewer
```

각 기능은 구현 전에 Guthub Issue로 추적 관리

이슈 제목 예시:

```text
feat: Implement ETRI style extractor
```

```text
fix: Proofing metadata remains in table cells
```

```text
feat: Add modern fallback table style
```

---

# 로드맵

## v3.0-alpha

* [x] Project structure
* [x] PySide6 GUI foundation
* [x] Multiple-file processing foundation
* [x] Proofing cleanup engine
* [x] Korean proofing-language support
* [x] Notes-removal support
* [ ] ETRI style extraction
* [ ] ETRI style application
* [ ] Template style-summary panel
* [ ] Stable executable build

## v3.1

* [ ] Theme extractor
* [ ] Master background extractor
* [ ] Background image optimizer
* [ ] Table style extractor
* [ ] Modern fallback table style
* [ ] Font normalization improvements

## v3.2

* [ ] Image optimizer
* [ ] Unused master cleanup
* [ ] PDF export
* [ ] CLI interface
* [ ] Style-profile manager

## v4.0

* [ ] Plugin system
* [ ] AI slide reviewer
* [ ] Presentation-quality report
* [ ] 3GPP document formatter
* [ ] Citation checker

---

# 라이선스

MIT License
