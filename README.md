# Advanced HWP MCP Server

고도화된 한글(HWP) MCP 서버 - 한글의 모든 기능을 제어할 수 있는 MCP 서버입니다.

## 설치 및 개발 상태 (2026-10-15)

- [Windows 설치 가이드](INSTALLATION_GUIDE.md): 최신 저장소 주소, 가상환경, 개인 경로 없는 설정 생성기
- [OSS 육성 계획](docs/OSS_REVIVAL_PLAN.md): 단계·검증 조건·신청 준비 기준
- [기여 안내](CONTRIBUTING.md): 버그 재현과 PR 제출
- MCP 서버 연결 자체는 한글 COM 객체를 즉시 실행하지 않으며, 실제 도구 요청에서 초기화합니다.
- `save_document(file_path=...)`는 한컴의 `SaveAs` 결과와 실제 파일 생성을 확인합니다.
- 위 구현 변경은 Windows에서의 실사용 테스트 전까지 **검증 중**입니다. GitHub CI는 모의 테스트이며 실제 한글 통합 성공을 뜻하지 않습니다.

## 🚀 주요 기능

### 기본 문서 제어
- ✅ 새 문서 생성 (`create_document`)
- ✅ 문서 열기 (`open_document`)
- ✅ 문서 저장 (`save_document`)
- ✅ 문서 정보 조회 (`get_document_info`)

### 고급 텍스트 조작
- ✅ 정밀한 텍스트 위치 지정 (`insert_text_at_position`)
- ✅ 텍스트 범위 선택 (`select_text_range`)
- ✅ 찾기/바꾸기 (`find_and_replace`)
- ✅ 일반 텍스트 삽입 (`insert_text`)

### 완전한 서식 제어
- ✅ 글꼴 서식 적용 (`apply_font_format`)
- ✅ 문단 서식 설정 (`set_paragraph_format`)
- ✅ 페이지 여백 설정 (`set_page_margins`)
- ✅ 용지 크기 및 방향 설정 (`set_page_size`)

### 표 기능
- ✅ 표 생성 (`create_table`)
- ✅ 셀 병합 (`merge_table_cells`)

### 객체 삽입
- ✅ 이미지 삽입 (`insert_image`)
- ✅ 도형 삽입 (`insert_shape`)
- ✅ 하이퍼링크 삽입 (`insert_hyperlink`)

### 문서 구조 관리
- ✅ 머리글/바닥글 삽입 (`insert_header_footer`)
- ✅ 페이지 나누기 (`insert_page_break`)
- ✅ 목차 생성 (`create_table_of_contents`)
- ✅ 제목 스타일 적용 (`apply_heading_style`)

### 고급 기능
- ✅ PDF 내보내기 (`export_to_pdf`)
- ✅ 한글 초기화 (`initialize_hwp`)

## 📋 필수 요구사항

### 시스템 요구사항
- **운영체제**: Windows (한글 프로그램 지원)
- **Python**: 3.10 이상
- **한글**: 한글 2010 이상 (HWPFrame.HwpObject 지원)

### 필수 패키지
```bash
python -m pip install -r requirements.txt
```

## 🛠️ 설치 및 설정

### 1. 패키지 설치
```bash
# 필수 패키지 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install mcp fastmcp pywin32
```

### 2. Claude Desktop 설정
Claude Desktop의 설정 파일에 다음 내용을 추가합니다:

**Windows 설정 파일 위치**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "advanced-hwp": {
      "command": "python",
      "args": [
        "G:/Ddrive/BatangD/task/workdiary/33MCP_HWP/advanced_hwp_server.py"
      ],
      "env": {
        "PYTHONPATH": "G:/Ddrive/BatangD/task/workdiary/33MCP_HWP"
      }
    }
  }
}
```

### 3. 한글 프로그램 설치 확인
- 한글 프로그램이 설치되어 있어야 합니다
- COM 객체 등록이 정상적으로 되어 있어야 합니다

## 🎯 사용 방법

### 기본 사용법
Claude Desktop에서 다음과 같이 요청하면 됩니다:

```
새 한글 문서를 만들고 "안녕하세요"라는 텍스트를 삽입해주세요.
```

### 고급 사용법

#### 1. 서식이 적용된 문서 생성
```
새 문서를 만들고 제목을 "보고서"로 하되 맑은고딕 18pt 굵게 설정하고, 
본문에 "내용입니다"를 바탕 12pt로 추가해주세요.
```

#### 2. 표가 포함된 문서
```
3행 4열 표를 만들고 첫 번째 행의 셀들을 병합해주세요.
```

#### 3. 이미지 삽입
```
C:\images\logo.png 이미지를 문서에 삽입하고 크기를 100x50mm로 설정해주세요.
```

#### 4. 페이지 설정
```
A4 용지를 가로 방향으로 설정하고 여백을 상하좌우 15mm로 설정해주세요.
```

## 📁 프로젝트 구조

```
33MCP_HWP/
├── advanced_hwp_server.py      # 메인 MCP 서버
├── requirements.txt            # 필수 패키지 목록
├── claude_desktop_config.json  # Claude Desktop 설정
├── README.md                   # 이 파일
├── 개발계획서.md              # 개발 계획서
└── 클로드코드프롬프트.md      # 개발 프롬프트
```

## 🔧 문제해결

### 1. 한글 초기화 실패
```
한글 프로그램이 설치되지 않았거나 초기화할 수 없습니다.
```
- 한글 프로그램이 설치되어 있는지 확인
- 한글을 한 번 실행해서 정상 동작하는지 확인
- COM 객체 등록 확인

### 2. 패키지 설치 오류
```
pip install pywin32
```
- 관리자 권한으로 실행
- 가상환경 사용 권장

### 3. Claude Desktop 연결 실패
- 설정 파일 경로가 정확한지 확인
- Python 경로가 올바른지 확인
- 방화벽 설정 확인

## 📊 성능 지표

- **초기화 시간**: < 3초
- **문서 생성 시간**: < 2초
- **서식 적용 시간**: < 1초
- **메모리 사용량**: < 50MB

## 🚧 알려진 제한사항

1. **Windows 전용**: 한글 프로그램의 특성상 Windows에서만 동작
2. **한글 필수**: 한글 프로그램이 설치되어 있어야 함
3. **COM 의존성**: Windows COM 객체에 의존

## 📈 향후 개선 계획

- [ ] 매크로 실행 기능 추가
- [ ] 차트 삽입 기능 추가
- [ ] 일괄 서식 적용 기능 강화
- [ ] 성능 최적화
- [ ] 오류 처리 개선

## 🤝 기여하기

이 프로젝트는 한국어 문서 작업의 자동화를 위한 프로젝트입니다. 
기여, 피드백, 이슈 리포트를 환영합니다!

## 📄 라이선스 상태

기존 README는 MIT 라이선스 배포를 표기했지만, **저장소에 정식 LICENSE 파일은 현재 없습니다.**
원 저작권·외부 코드의 권리를 확인하고 유지관리자의 공개 라이선스 결정을 거친 후 정식 파일을 추가해야 합니다.
현재 이 문구만으로 제3자에게 MIT 이용 권한이 부여되었다고 판단해서는 안 됩니다.

---

**참고**: 이 MCP 서버는 기존의 기본 한글 MCP 서버 대비 10배 이상 많은 기능을 제공합니다.