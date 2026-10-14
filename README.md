# Advanced HWP MCP

> AI 에이전트가 **한컴오피스 한글(HWP)** 문서를 생성·편집·저장하도록 연결하는 MCP(Model Context Protocol) 도구입니다.
>
> *A Model Context Protocol server for controlling Korean Hangul (HWP) documents. Workflow automation and format conversion are experimental directions, currently under viability review.*

## 방향 재검토 — 2026-10-15

**현재 결정: 사용자 문제 해결과 OSS 경쟁력 검증이 먼저이며, 로컬 33·34·35의 대규모 통합 개발은 잠정 보류합니다.**

이 저장소를 폐기하거나 새 저장소로 이동하는 결정은 아닙니다. 기존 사용자 [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1)의 자동 실행·저장 문제, Windows COM 안정성, 타 도구 대비 실제 장점을 먼저 확인하겠습니다.

- **ACTIVE:** [#5 기존 사용자 오류](https://github.com/skerishKang/33MCP_HWP_Limone/issues/5), [#11 Windows 실기](https://github.com/skerishKang/33MCP_HWP_Limone/issues/11), [#16 OSS 가치·차별화 판단](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16).
- **HOLD:** 자동화/변환 대규모 확장, 설치 GUI, 템플릿, 일괄 처리, 변경 비교 기능. 이미 작성한 코드와 이슈는 보존합니다.
- **Draft PR #2:** 신규 도구는 기본 비활성이고 로컬 테스트·GitHub CI는 통과했지만, 실제 한글 COM 테스트에서 오류가 발생하여 실사용 검증 미완료입니다. Ready/merge/release하지 않습니다.
- **의사결정:** 실제 사용자와 대체 도구 비교 후 INVEST(계속 개발) / MAINTAIN(필수 유지보수) / PIVOT(다른 기술·OSS 기여에 집중)을 근거 기반으로 선택합니다.

[검증 기준](docs/OSS_FIT_REVIEW.md) · [최신 로드맵](docs/ROADMAP.md) · [이슈 보드](docs/ISSUE_INDEX.md)

> 아래의 33·34·35 통합 구조는 **이전 설계안/조건부 후보**입니다. 확정된 개발 일정이나 완료된 기능으로 보지 마세요.

[Issues](https://github.com/skerishKang/33MCP_HWP_Limone/issues) · [통합 프로젝트 #3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3) · [개발 로드맵](docs/ROADMAP.md) · [운영 문서](docs/OPERATIONS.md)

## 프로젝트 현황 (2026-10-15)

**공식 저장소는 이곳 하나입니다.** 로컬 `workdiary/33-MCP_HWP`, `34-hwp-automation`, `35-hwp-pdf-html`의 실효성 있는 기능을 선별해 통합하는 프로젝트입니다. **세 로컬 프로젝트가 GitHub에 통합되었다는 뜻은 아닙니다.**

| 구분 | 현재 상태 | 앞으로의 작업 |
|---|---|---|
| **33: HWP 문서 제어** | GitHub `main`에 기존 MCP + HWP COM 코드. 외부 사용자 버그 [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1)이 열려 있음 | 실제 Windows/HWP 저장·재열기 검증, 로컬 향상 버전 검토 |
| **34: HWP 작업 자동화** | 로컬에 액션·백업·롤백 뼈대가 존재. 일부 표/저널 메서드는 스텁 | 실제 편집·멱등성·롤백 동작 완성 |
| **35: 문서 변환** | 로컬에 HWP→PDF→HTML, PDF→HTML 설계/코드 존재. 기존 평가 수치는 시뮬레이션 | 실행 경로 완성, 실측 정확도 테스트 |
| **설치/품질 개선** | [Draft PR #2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2)에서 초기화 지연, 저장 확인, 설치 안내, mock CI 준비 | Windows 실제 HWP 검증 후 반영 |
| **OSS 운영** | 이슈·설계/운영/검증 문서 정비 중 | 저작권/라이선스 결정, 첫 검증 릴리스, 사용자 피드백 |

**주의:** 기존 README의 '25개 모든 도구 완전 동작', '10배 향상', '초기화 3초 이내' 등 표현은 측정·실기 증거가 없어 검증된 성능으로 취급하지 않습니다. 설치 후 실제 문서로 확인하기 전까지 중요한 고객 자료를 사용하지 마세요.

## 세 가지 모듈의 기존 통합 구상 (현재 HOLD)

```text
Claude Desktop / Gemini CLI / 검증된 기타 MCP 클라이언트
                   |
             MCP stdio 서버
          advanced_hwp_server.py   <- 기존 진입점 유지
                   |
       공통 COM 세션 / 파일 경계
         /          |           \
    33 문서 제어  34 일괄 자동화  35 문서 변환
```

현재 구조와 계획 상세: [아키텍처](docs/ARCHITECTURE.md), [소스 인벤토리](docs/PROJECT_INVENTORY.md), [설계 의사결정](docs/DECISIONS.md).

### 기존 구현 영역 (실기 검증 필요)
- 문서 생성/열기/저장, 일반 텍스트 편집
- 문단·글꼴·표·이미지 등 HWP COM 조작 기능의 일부
- Windows에서 `HWPFrame.HwpObject` 사용. **한컴오피스 한글이 설치되어 있어야 합니다.**

### 통합 후보 (현재 HOLD · 구현 완료 아님)
- 34: 여러 동작을 한 작업으로 실행, 중복 실행 방지, 원본 보존, 백업·복구
- 35: HWP→PDF→HTML / PDF→HTML 변환; 스캔 문서 OCR은 선택 기능
- 템플릿 기반 공문·보고서·계약서 작성, 여러 문서 일괄 작업, 변경 전후 비교

## 실험 기능 개발 현황 (Draft PR #2, 기본 비활성)

로컬 34·35의 설계를 참고하여 기능을 **작동 가능한 작은 단위부터** 개발하고 있습니다. 아직 안정 릴리스가 아닙니다.

- `replace_document_text(input_path, output_path, replacements)`: 기존 HWP에서 문자열을 찾아 다른 새 HWP로 저장하는 일괄 처리 프로토타입. 원본 덮어쓰기 금지, 텍스트 전후 확인 시도. **실제 Windows/HWP 실기 테스트에서 아직 실패 중**입니다.
- `convert_pdf_to_html(pdf_path, output_dir, mode="editable")`: 텍스트 기반 PDF에서 실제 텍스트를 추출해 HTML 작성. 합성 PDF로 성공 확인. `mode`는 `editable` 또는 `faithful`(대략적인 배치)입니다. OCR·표/이미지·폰트의 정밀 보존은 불가합니다.
- `convert_hwp_to_html(hwp_path, output_dir, mode="editable")`: HWP→PDF→HTML 변환 경로. **HWP COM 실기 검증 실패/미완료**, 현재는 모의 COM 경로만 테스트했습니다.

위 세 도구는 **`HWP_MCP_ENABLE_EXPERIMENTAL=1`을 명시적으로 설정한 경우에만 MCP 도구 목록에 등록**됩니다. 기본 설치로는 노출되지 않습니다. 새로운 HWP COM 작업은 별도 Python 작업 프로세스에서 실행해 충돌이 발생해도 MCP 서버가 종료되지 않도록 격리합니다. **COM 오류 자체가 해결된 것은 아니므로**, 새 HWP 기능의 실험은 별도 테스트 PC에서만 권장합니다.

PDF 추출 라이브러리는 선택 설치합니다.

```powershell
py -m pip install -r requirements-convert.txt
```

개발 내용·성공/실패 검증 기록: [PHASE1_DEV_STATUS](docs/PHASE1_DEV_STATUS.md).

## 설치와 사용

현재 기본 브랜치의 `requirements.txt`에는 별도 설치 대상이 아닌 `pythoncom`이 포함되어 있으며, 설치 가이드의 일부 복사 예제에는 과거 PC 경로가 있습니다. **그대로 실행하는 설치 가이드를 정상 작동한다고 보증하지 않습니다.** 해당 보완은 [Draft PR #2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2)에 있습니다.

지원 목표는 Windows 10/11 + 한컴오피스 한글 + Python 3.10 이상입니다. 필요한 환경에서는 Python MCP SDK와 `pywin32`를 사용합니다.

초기 실사용 수락 시나리오:
1. 클라이언트에 `advanced_hwp_server.py`를 MCP `stdio` 서버로 등록합니다.
2. 연결만으로 한글을 실행하지 않는지 확인합니다(기존 `main`은 이 문제가 보고된 상태입니다).
3. AI에게 새 문서 생성과 가상의 텍스트 입력을 요청합니다.
4. 존재하는 출력 폴더의 절대 경로로 HWP 저장을 요청합니다.
5. 파일이 실제로 생성되고 한글에서 다시 열리는지 확인합니다.

자세한 운영·문제해결: [OPERATIONS](docs/OPERATIONS.md) · [TEST_PLAN](docs/TEST_PLAN.md).

## 협업과 공개 개발

- [개발 작업 전체](docs/ISSUE_INDEX.md) · [통합 에픽 #3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3)
- [AGENTS.md](AGENTS.md): 새 개발 세션이 확인해야 할 작업 원칙
- [CONTRIBUTING.md](CONTRIBUTING.md): 이슈·PR 작성, 실기 증거, 데이터 보호
- [SECURITY.md](SECURITY.md): 취약점 신고
- [SECURITY_AND_LICENSE](docs/SECURITY_AND_LICENSE.md): 공개 전 점검/권리
- [RELEASE_PROCESS](docs/RELEASE_PROCESS.md): 릴리스·복구 기준

버그 보고 시 Windows, Python, HWP, MCP 클라이언트 버전과 재현 단계를 알려 주세요. 개인정보·인증정보·실제 고객 문서는 올리지 마세요.

## 라이선스 상태

과거 GitHub README는 MIT라고 설명했지만 현재 GitHub `main`에는 정식 `LICENSE` 파일이 없습니다. 로컬 33번에는 별도의 MIT 파일이 존재합니다. **그 파일을 그대로 GitHub 전체의 라이선스로 확정하거나 34·35번 코드까지 자동 적용하지 않습니다.** 소스 출처·저작권을 검토한 다음 프로젝트 소유자가 공개 조건을 결정합니다([#10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10)).

---

**English quick summary:** This repository currently contains a Windows COM-based MCP server for Hancom Hangul. Unifying local editing (33), automation (34), and conversion (35) is a **paused proposal, not a shipped release or mandatory roadmap**. Windows end-to-end compatibility, source licensing and packaging remain under review. Please see the linked issues and documentation for accurately scoped capabilities.
