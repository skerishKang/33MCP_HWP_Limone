# Advanced HWP MCP Server — Windows 설치 및 검증

이 문서는 현재 저장소 `skerishKang/33MCP_HWP_Limone`의 코드를 기준으로 합니다.
실제 HWP COM 통합은 Windows + 한컴오피스 한글 설치 환경에서만 검증할 수 있습니다.

## 준비물

- Windows, Python 3.10 이상, 설치된 한글(HWPFrame.HwpObject COM 등록)
- MCP 표준 입출력(stdio)을 연결할 수 있는 클라이언트 (예: Claude Desktop, Gemini CLI)
- Python 설치 시 PATH 또는 `py` 런처 사용 가능
- 한글 자동화의 라이선스와 파일 접근 경고 등 사용 환경의 조건 확인

## 1. 내려받고 가상환경 만들기

PowerShell에서 실행합니다.

```powershell
git clone https://github.com/skerishKang/33MCP_HWP_Limone.git
cd 33MCP_HWP_Limone
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`pythoncom`은 별도 pip 패키지가 아닙니다. Windows에서 `pywin32`가 제공합니다.

## 2. 내 PC에 맞는 MCP 설정 생성

```powershell
.\.venv\Scripts\python.exe scripts\generate_mcp_config.py
```

출력된 `mcpServers` JSON을 사용하는 MCP 클라이언트 설정에 **병합**합니다.
예: Claude Desktop의 사용자 설정 `%APPDATA%\Claude\claude_desktop_config.json`.
다른 서버 설정이 있다면 파일 전체를 덮어쓰지 마세요.

- 생성기는 로컬 Python 실행 경로와 서버 파일의 절대 경로를 자동으로 계산합니다.
- 생성기는 설정 파일에 쓰지 않습니다. 출력 내용을 검토한 뒤 사용자가 직접 반영합니다.
- Gemini CLI 등 다른 MCP 클라이언트는 해당 제품의 구성 방식에 맞게 `command`와 `args`를 사용합니다.
- 이전 예제의 개인 컴퓨터 경로는 사용하지 마세요.

## 3. 실행 확인

클라이언트를 재시작한 뒤 다음 순서대로 확인합니다.

1. MCP 서버 연결만으로 한글 창이 실행되지 않는지 확인
2. AI에 "새 한글 문서를 생성해 주세요"라고 요청 (이 시점에 한글이 실행될 수 있음)
3. 텍스트를 입력한 다음 **절대 경로**로 저장 요청
4. 지정된 위치에 크기가 0보다 큰 `.hwp` 파일이 존재하는지 탐색기에서 확인
5. 한글 프로그램으로 다시 열어 내용과 서식이 정상인지 확인

파일 저장 예:
`C:\Users\<사용자계정>\Documents\mcp-example.hwp`

새 문서를 저장할 때는 `save_document(file_path=...)`에 경로를 전달해야 합니다.
기본 `save_document()`는 새 문서에서 저장 대화상자에 의존하지 않도록 실패 메시지로 경로를 요청합니다.
지정한 디렉터리가 없으면 먼저 만들어야 합니다.

## 4. 테스트의 의미

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe test_hwp_server.py
```

- 첫 번째 명령은 HWP 없이 돌아가는 모의(mock) 회귀 테스트입니다.
- 두 번째는 실제 한글 COM을 실행하고 `test_document.hwp`를 생성할 수 있는 **수동 실기 검증**입니다.
- Windows 실기 테스트를 수행하지 않았다면 "실사용 검증 완료"라고 표시하지 않습니다.
- 회사·고객의 실제 문서를 테스트에 사용하지 마세요.

## 5. 오류 진단

- MCP 연결 즉시 한글이 실행된다면 **설치한 서버 코드가 최신인지** 확인해 주세요.
- 저장 실패라면 출력 경로, 폴더 존재 여부, 권한, 한글의 파일 접근 경고를 확인해 주세요.
- COM 초기화 실패라면 한글 설치·COM 등록 상태를 확인해 주세요.
- 기능별 호환성 문제는 한글 버전·Python 버전·클라이언트 버전과 재현 순서를 GitHub Issue에 남겨 주세요.

현재 실기 검증 범위는 제한적입니다. 모든 HWP 버전과 모든 MCP 클라이언트에 대한 호환성을 보증하지 않습니다.
