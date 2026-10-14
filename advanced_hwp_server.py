#!/usr/bin/env python3
"""
Advanced HWP MCP Server
고도화된 한글 MCP 서버 - 한글의 모든 기능을 제어할 수 있는 MCP 서버
"""

import logging
import sys
import os
from typing import Optional, Dict, Any, List, Tuple
import json

try:
    from mcp.server.fastmcp import FastMCP
    import win32com.client
    import pythoncom
    import win32api
    import win32con
except ImportError as e:
    print(f"필수 패키지가 설치되지 않음: {e}", file=sys.stderr)
    print("다음 명령어로 패키지를 설치하세요:", file=sys.stderr)
    print("pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# MCP stdio is a protocol channel: diagnostics go to stderr only.
# Never create a log file in the client's arbitrary working directory on import.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# MCP 서버 초기화
mcp = FastMCP("Advanced HWP Server")

class AdvancedHwpController:
    """고급 한글 컨트롤러 클래스"""
    
    def __init__(self):
        """한글 COM 객체 초기화"""
        self.hwp = None
        self.is_initialized = False
        self.current_document = None
        
    def initialize(self):
        """한글 COM 객체 초기화"""
        try:
            pythoncom.CoInitialize()
            
            # 한글 프로그램이 설치되어 있는지 확인
            try:
                self.hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
            except:
                # gencache가 실패하면 일반 Dispatch 사용
                self.hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
            
            # 한글 창을 보이게 설정
            if self.hwp.XHwpWindows.Count > 0:
                self.hwp.XHwpWindows.Item(0).Visible = True
            
            self.is_initialized = True
            logger.info("한글 COM 객체 초기화 완료")
            return True
            
        except Exception as e:
            logger.error(f"한글 COM 객체 초기화 실패: {e}")
            return False
    
    def __del__(self):
        """리소스 정리"""
        try:
            if self.is_initialized:
                pythoncom.CoUninitialize()
        except:
            pass
    
    def check_initialization(self):
        """초기화 상태 확인"""
        if not self.is_initialized:
            if not self.initialize():
                raise Exception("한글 프로그램이 설치되지 않았거나 초기화할 수 없습니다.")
        return True

# 전역 컨트롤러 인스턴스
hwp_controller = AdvancedHwpController()

@mcp.tool()
def initialize_hwp() -> str:
    """한글 프로그램을 초기화합니다."""
    try:
        if hwp_controller.initialize():
            return "한글 프로그램 초기화 성공"
        else:
            return "한글 프로그램 초기화 실패"
    except Exception as e:
        logger.error(f"초기화 중 오류: {e}")
        return f"초기화 실패: {e}"

@mcp.tool()
def create_document() -> str:
    """새 한글 문서를 생성합니다."""
    try:
        hwp_controller.check_initialization()
        
        # COM returns False on failure; do not report a new document otherwise.
        if not hwp_controller.hwp.HAction.Run("FileNew"):
            return "문서 생성 실패: 한글 FileNew 명령이 실패했습니다."
        hwp_controller.current_document = "new_document"
        
        logger.info("새 문서 생성 완료")
        return "새 문서가 생성되었습니다."
        
    except Exception as e:
        logger.error(f"문서 생성 실패: {e}")
        return f"문서 생성 실패: {e}"

@mcp.tool()
def open_document(file_path: str) -> str:
    """지정된 경로의 한글 문서를 엽니다."""
    try:
        # Reject missing/unreadable paths before launching Hangul.
        if not os.path.isfile(file_path):
            return f"파일을 찾을 수 없습니다: {file_path}"
        hwp_controller.check_initialization()

        # A successful Execute return is required before claiming an open.
        act = hwp_controller.hwp.CreateAction("FileOpen")
        pset = act.CreateSet()
        pset.SetItem("filename", file_path)
        if not act.Execute(pset):
            return f"문서 열기 실패: 한글 FileOpen 명령이 실패했습니다: {file_path}"

        hwp_controller.current_document = file_path
        logger.info(f"문서 열기 완료: {file_path}")
        return f"문서를 열었습니다: {file_path}"
        
    except Exception as e:
        logger.error(f"문서 열기 실패: {e}")
        return f"문서 열기 실패: {e}"

@mcp.tool()
def save_document(file_path: Optional[str] = None) -> str:
    """현재 문서를 저장합니다. 새 문서는 저장할 파일 경로를 지정해야 합니다."""
    try:
        hwp_controller.check_initialization()

        if file_path:
            target = os.path.abspath(os.path.expanduser(file_path))
            parent = os.path.dirname(target)
            if not os.path.isdir(parent):
                return f"문서 저장 실패: 대상 폴더가 존재하지 않습니다: {parent}"

            # 공식 HwpObject COM API의 SaveAs를 사용한다.
            # 성공 반환값뿐 아니라 디스크의 결과 파일까지 확인한다.
            result = hwp_controller.hwp.SaveAs(target, "HWP", "")
            if not result:
                return f"문서 저장 실패: 한글 SaveAs가 실패를 반환했습니다: {target}"
            if not os.path.isfile(target) or os.path.getsize(target) == 0:
                return f"문서 저장 실패: 저장된 파일을 확인할 수 없습니다: {target}"

            hwp_controller.current_document = target
            logger.info("문서 저장 완료: %s", target)
            return f"문서를 저장했습니다: {target}"

        if hwp_controller.current_document in (None, "new_document"):
            return "문서 저장 실패: 새 문서는 file_path에 저장할 .hwp 전체 경로를 지정해주세요."

        result = hwp_controller.hwp.HAction.Run("FileSave")
        if not result:
            return "문서 저장 실패: 한글 FileSave가 실패를 반환했습니다."

        target = hwp_controller.current_document
        if not os.path.isfile(target) or os.path.getsize(target) == 0:
            return f"문서 저장 실패: 저장된 파일을 확인할 수 없습니다: {target}"

        logger.info("문서 저장 완료: %s", target)
        return f"문서를 저장했습니다: {target}"

    except Exception as e:
        logger.error("문서 저장 실패: %s", e)
        return f"문서 저장 실패: {e}"

@mcp.tool()
def insert_text(text: str, position: str = "current") -> str:
    """텍스트를 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        if position == "current":
            # 현재 위치에 텍스트 삽입
            act = hwp_controller.hwp.CreateAction("InsertText")
            pset = act.CreateSet()
            pset.SetItem("Text", text)
            act.Execute(pset)
        
        logger.info(f"텍스트 삽입 완료: {text[:50]}...")
        return f"텍스트를 삽입했습니다: {text[:50]}..."
        
    except Exception as e:
        logger.error(f"텍스트 삽입 실패: {e}")
        return f"텍스트 삽입 실패: {e}"

@mcp.tool()
def insert_text_at_position(text: str, x: int = 0, y: int = 0) -> str:
    """지정된 좌표에 텍스트를 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 좌표로 커서 이동
        hwp_controller.hwp.SetPosBySet(x, y)
        
        # 텍스트 삽입
        act = hwp_controller.hwp.CreateAction("InsertText")
        pset = act.CreateSet()
        pset.SetItem("Text", text)
        act.Execute(pset)
        
        logger.info(f"위치 ({x}, {y})에 텍스트 삽입 완료")
        return f"위치 ({x}, {y})에 텍스트 '{text}'를 삽입했습니다."
        
    except Exception as e:
        logger.error(f"위치별 텍스트 삽입 실패: {e}")
        return f"위치별 텍스트 삽입 실패: {e}"

@mcp.tool()
def apply_font_format(font_name: str = "맑은 고딕", 
                     font_size: int = 11, 
                     bold: bool = False, 
                     italic: bool = False, 
                     underline: bool = False,
                     color: str = "black") -> str:
    """선택된 텍스트에 글꼴 서식을 적용합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 색상 변환
        color_map = {
            "black": 0x000000,
            "red": 0xFF0000,
            "blue": 0x0000FF,
            "green": 0x00FF00,
            "yellow": 0xFFFF00,
            "purple": 0xFF00FF,
            "cyan": 0x00FFFF
        }
        
        color_value = color_map.get(color.lower(), 0x000000)
        
        # 글꼴 서식 적용
        act = hwp_controller.hwp.CreateAction("CharShape")
        pset = act.CreateSet()
        pset.SetItem("FaceNameHangul", font_name)
        pset.SetItem("FaceNameLatin", font_name)
        pset.SetItem("FaceNameHanja", font_name)
        pset.SetItem("FaceNameJapanese", font_name)
        pset.SetItem("FaceNameOther", font_name)
        pset.SetItem("FaceNameSymbol", font_name)
        pset.SetItem("FaceNameUser", font_name)
        pset.SetItem("Height", font_size * 100)  # 한글에서는 포인트 * 100
        pset.SetItem("Bold", bold)
        pset.SetItem("Italic", italic)
        pset.SetItem("Underline", underline)
        pset.SetItem("TextColor", color_value)
        act.Execute(pset)
        
        logger.info(f"글꼴 서식 적용 완료: {font_name}, {font_size}pt")
        return f"글꼴 서식을 적용했습니다: {font_name}, {font_size}pt"
        
    except Exception as e:
        logger.error(f"글꼴 서식 적용 실패: {e}")
        return f"글꼴 서식 적용 실패: {e}"

@mcp.tool()
def select_text_range(start_pos: int, end_pos: int) -> str:
    """지정된 범위의 텍스트를 선택합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 시작 위치로 이동
        hwp_controller.hwp.SetPos(start_pos)
        
        # 드래그하여 텍스트 선택
        hwp_controller.hwp.MovePos(2, end_pos - start_pos, 1)  # 2: 오른쪽, 1: 선택
        
        logger.info(f"텍스트 선택 완료: {start_pos} ~ {end_pos}")
        return f"텍스트를 선택했습니다: 위치 {start_pos} ~ {end_pos}"
        
    except Exception as e:
        logger.error(f"텍스트 선택 실패: {e}")
        return f"텍스트 선택 실패: {e}"

@mcp.tool()
def find_and_replace(find_text: str, replace_text: str, replace_all: bool = False) -> str:
    """텍스트를 찾아서 바꿉니다."""
    try:
        hwp_controller.check_initialization()
        
        # 찾기/바꾸기 실행
        act = hwp_controller.hwp.CreateAction("Replace")
        pset = act.CreateSet()
        pset.SetItem("FindString", find_text)
        pset.SetItem("ReplaceString", replace_text)
        pset.SetItem("ReplaceMode", 1 if replace_all else 0)  # 0: 찾기, 1: 모두 바꾸기
        result = act.Execute(pset)
        
        if result:
            logger.info(f"찾기/바꾸기 완료: '{find_text}' → '{replace_text}'")
            return f"'{find_text}'를 '{replace_text}'로 {'모두 ' if replace_all else ''}바꾸었습니다."
        else:
            return f"'{find_text}'를 찾을 수 없습니다."
            
    except Exception as e:
        logger.error(f"찾기/바꾸기 실패: {e}")
        return f"찾기/바꾸기 실패: {e}"

@mcp.tool()
def create_table(rows: int, cols: int, border: bool = True) -> str:
    """표를 생성합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 표 생성
        act = hwp_controller.hwp.CreateAction("TableCreate")
        pset = act.CreateSet()
        pset.SetItem("Rows", rows)
        pset.SetItem("Cols", cols)
        pset.SetItem("WidthType", 2)  # 2: 문서 너비에 맞춤
        pset.SetItem("HeightType", 0)  # 0: 자동
        pset.SetItem("CreateItemArray", [0, 1, 0])  # 기본 설정
        act.Execute(pset)
        
        logger.info(f"표 생성 완료: {rows}행 {cols}열")
        return f"{rows}행 {cols}열 표를 생성했습니다."
        
    except Exception as e:
        logger.error(f"표 생성 실패: {e}")
        return f"표 생성 실패: {e}"

@mcp.tool()
def set_page_margins(top: int = 20, bottom: int = 20, left: int = 20, right: int = 20) -> str:
    """페이지 여백을 설정합니다. (단위: mm)"""
    try:
        hwp_controller.check_initialization()
        
        # 페이지 설정
        act = hwp_controller.hwp.CreateAction("PageSetup")
        pset = act.CreateSet()
        pset.SetItem("TopMargin", top * 100)  # 한글에서는 mm * 100
        pset.SetItem("BottomMargin", bottom * 100)
        pset.SetItem("LeftMargin", left * 100)
        pset.SetItem("RightMargin", right * 100)
        act.Execute(pset)
        
        logger.info(f"페이지 여백 설정 완료: 상{top} 하{bottom} 좌{left} 우{right}mm")
        return f"페이지 여백을 설정했습니다: 상{top} 하{bottom} 좌{left} 우{right}mm"
        
    except Exception as e:
        logger.error(f"페이지 여백 설정 실패: {e}")
        return f"페이지 여백 설정 실패: {e}"

@mcp.tool()
def get_document_info() -> str:
    """현재 문서의 정보를 조회합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 문서 정보 수집 (실제 API에 맞게 수정)
        try:
            page_count = hwp_controller.hwp.PageCount  # 속성으로 접근
        except:
            page_count = "Unknown"
            
        try:
            current_pos = hwp_controller.hwp.GetPos()
        except:
            current_pos = "Unknown"
            
        # 현재 페이지는 계산으로 구하기
        try:
            # ListCount를 사용해서 전체 리스트 정보 확인
            list_count = getattr(hwp_controller.hwp, 'ListCount', 0)
        except:
            list_count = "Unknown"
        
        info = {
            "page_count": page_count,
            "current_pos": current_pos,
            "list_count": list_count,
            "document_name": hwp_controller.current_document or "새 문서"
        }
        
        result = f"""문서 정보:
- 문서명: {info['document_name']}
- 총 페이지 수: {info['page_count']}
- 현재 커서 위치: {info['current_pos']}
- 리스트 개수: {info['list_count']}"""
        
        logger.info("문서 정보 조회 완료")
        return result
        
    except Exception as e:
        logger.error(f"문서 정보 조회 실패: {e}")
        return f"문서 정보 조회 실패: {e}"

@mcp.tool()
def set_paragraph_format(align: str = "left", 
                        left_indent: int = 0, 
                        right_indent: int = 0, 
                        line_spacing: float = 1.0) -> str:
    """문단 서식을 설정합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 정렬 방식 변환
        align_map = {
            "left": 0,
            "center": 1,
            "right": 2,
            "justify": 3,
            "distribute": 4
        }
        
        align_value = align_map.get(align.lower(), 0)
        
        # 문단 서식 설정
        act = hwp_controller.hwp.CreateAction("ParagraphShape")
        pset = act.CreateSet()
        pset.SetItem("Align", align_value)
        pset.SetItem("IndentLeft", left_indent * 100)  # mm * 100
        pset.SetItem("IndentRight", right_indent * 100)
        pset.SetItem("LineSpacing", int(line_spacing * 100))
        act.Execute(pset)
        
        logger.info(f"문단 서식 설정 완료: {align} 정렬, 줄간격 {line_spacing}")
        return f"문단 서식을 설정했습니다: {align} 정렬, 줄간격 {line_spacing}"
        
    except Exception as e:
        logger.error(f"문단 서식 설정 실패: {e}")
        return f"문단 서식 설정 실패: {e}"

@mcp.tool()
def set_page_size(width: int = 210, height: int = 297, orientation: str = "portrait") -> str:
    """용지 크기와 방향을 설정합니다. (단위: mm)"""
    try:
        hwp_controller.check_initialization()
        
        # 용지 방향 처리
        if orientation.lower() == "landscape":
            width, height = height, width
        
        # 페이지 설정
        act = hwp_controller.hwp.CreateAction("PageSetup")
        pset = act.CreateSet()
        pset.SetItem("Width", width * 100)  # mm * 100
        pset.SetItem("Height", height * 100)
        pset.SetItem("Orientation", 1 if orientation.lower() == "landscape" else 0)
        act.Execute(pset)
        
        logger.info(f"용지 설정 완료: {width}x{height}mm, {orientation}")
        return f"용지를 설정했습니다: {width}x{height}mm, {orientation}"
        
    except Exception as e:
        logger.error(f"용지 설정 실패: {e}")
        return f"용지 설정 실패: {e}"

@mcp.tool()
def insert_image(image_path: str, x: int = 0, y: int = 0, width: int = 100, height: int = 100) -> str:
    """이미지를 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        if not os.path.exists(image_path):
            return f"이미지 파일을 찾을 수 없습니다: {image_path}"
        
        # 이미지 삽입
        act = hwp_controller.hwp.CreateAction("InsertPicture")
        pset = act.CreateSet()
        pset.SetItem("Path", image_path)
        pset.SetItem("Embedded", True)
        pset.SetItem("sizeoption", 3)  # 사용자 정의 크기
        pset.SetItem("Width", width * 100)  # mm * 100
        pset.SetItem("Height", height * 100)
        act.Execute(pset)
        
        logger.info(f"이미지 삽입 완료: {image_path}")
        return f"이미지를 삽입했습니다: {image_path}"
        
    except Exception as e:
        logger.error(f"이미지 삽입 실패: {e}")
        return f"이미지 삽입 실패: {e}"

@mcp.tool()
def insert_shape(shape_type: str, x: int = 0, y: int = 0, width: int = 50, height: int = 50) -> str:
    """도형을 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 도형 종류 맵핑
        shape_map = {
            "rectangle": 1,
            "ellipse": 2,
            "line": 3,
            "arrow": 4,
            "textbox": 5
        }
        
        shape_value = shape_map.get(shape_type.lower(), 1)
        
        # 도형 삽입
        act = hwp_controller.hwp.CreateAction("DrawObjDialog")
        pset = act.CreateSet()
        pset.SetItem("ShapeType", shape_value)
        pset.SetItem("TreatAsChar", False)
        act.Execute(pset)
        
        logger.info(f"도형 삽입 완료: {shape_type}")
        return f"도형을 삽입했습니다: {shape_type}"
        
    except Exception as e:
        logger.error(f"도형 삽입 실패: {e}")
        return f"도형 삽입 실패: {e}"

@mcp.tool()
def insert_header_footer(text: str, is_header: bool = True, position: str = "center") -> str:
    """머리글 또는 바닥글을 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 머리글/바닥글 편집 모드 진입
        if is_header:
            hwp_controller.hwp.HAction.Run("HeaderFooterEdit")
        else:
            hwp_controller.hwp.HAction.Run("HeaderFooterEdit")
        
        # 텍스트 삽입
        act = hwp_controller.hwp.CreateAction("InsertText")
        pset = act.CreateSet()
        pset.SetItem("Text", text)
        act.Execute(pset)
        
        # 편집 모드 종료
        hwp_controller.hwp.HAction.Run("CloseEx")
        
        logger.info(f"{'머리글' if is_header else '바닥글'} 삽입 완료")
        return f"{'머리글' if is_header else '바닥글'}을 삽입했습니다: {text}"
        
    except Exception as e:
        logger.error(f"머리글/바닥글 삽입 실패: {e}")
        return f"머리글/바닥글 삽입 실패: {e}"

@mcp.tool()
def insert_page_break() -> str:
    """페이지 나누기를 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 페이지 나누기 삽입
        act = hwp_controller.hwp.CreateAction("BreakPage")
        act.Execute()
        
        logger.info("페이지 나누기 삽입 완료")
        return "페이지 나누기를 삽입했습니다."
        
    except Exception as e:
        logger.error(f"페이지 나누기 삽입 실패: {e}")
        return f"페이지 나누기 삽입 실패: {e}"

@mcp.tool()
def merge_table_cells(start_row: int, start_col: int, end_row: int, end_col: int) -> str:
    """표의 셀을 병합합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 셀 범위 선택
        hwp_controller.hwp.TableCellBlock(start_row, start_col, end_row, end_col)
        
        # 셀 병합
        act = hwp_controller.hwp.CreateAction("TableMergeCell")
        act.Execute()
        
        logger.info(f"셀 병합 완료: ({start_row},{start_col}) ~ ({end_row},{end_col})")
        return f"셀을 병합했습니다: ({start_row},{start_col}) ~ ({end_row},{end_col})"
        
    except Exception as e:
        logger.error(f"셀 병합 실패: {e}")
        return f"셀 병합 실패: {e}"

@mcp.tool()
def insert_hyperlink(text: str, url: str) -> str:
    """하이퍼링크를 삽입합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 하이퍼링크 삽입
        act = hwp_controller.hwp.CreateAction("InsertHyperlink")
        pset = act.CreateSet()
        pset.SetItem("Text", text)
        pset.SetItem("URL", url)
        act.Execute(pset)
        
        logger.info(f"하이퍼링크 삽입 완료: {text} -> {url}")
        return f"하이퍼링크를 삽입했습니다: {text} -> {url}"
        
    except Exception as e:
        logger.error(f"하이퍼링크 삽입 실패: {e}")
        return f"하이퍼링크 삽입 실패: {e}"

@mcp.tool()
def create_table_of_contents() -> str:
    """목차를 생성합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 목차 삽입
        act = hwp_controller.hwp.CreateAction("InsertTableOfContents")
        pset = act.CreateSet()
        pset.SetItem("AutoUpdate", True)
        pset.SetItem("ShowPageNum", True)
        act.Execute(pset)
        
        logger.info("목차 생성 완료")
        return "목차를 생성했습니다."
        
    except Exception as e:
        logger.error(f"목차 생성 실패: {e}")
        return f"목차 생성 실패: {e}"

@mcp.tool()
def apply_heading_style(level: int, text: str) -> str:
    """제목 스타일을 적용합니다."""
    try:
        hwp_controller.check_initialization()
        
        # 텍스트 삽입
        act = hwp_controller.hwp.CreateAction("InsertText")
        pset = act.CreateSet()
        pset.SetItem("Text", text)
        act.Execute(pset)
        
        # 제목 스타일 적용
        style_name = f"제목 {level}"
        act = hwp_controller.hwp.CreateAction("StyleApply")
        pset = act.CreateSet()
        pset.SetItem("StyleName", style_name)
        act.Execute(pset)
        
        logger.info(f"제목 스타일 적용 완료: {style_name}")
        return f"제목 스타일을 적용했습니다: {style_name}"
        
    except Exception as e:
        logger.error(f"제목 스타일 적용 실패: {e}")
        return f"제목 스타일 적용 실패: {e}"

@mcp.tool()
def export_to_pdf(output_path: str) -> str:
    """현재 문서를 PDF로 내보냅니다."""
    try:
        hwp_controller.check_initialization()
        
        # PDF 내보내기
        act = hwp_controller.hwp.CreateAction("FileSaveAsPdf")
        pset = act.CreateSet()
        pset.SetItem("filename", output_path)
        pset.SetItem("Format", "PDF")
        act.Execute(pset)
        
        logger.info(f"PDF 내보내기 완료: {output_path}")
        return f"PDF로 내보냈습니다: {output_path}"
        
    except Exception as e:
        logger.error(f"PDF 내보내기 실패: {e}")
        return f"PDF 내보내기 실패: {e}"

def replace_document_text(
    input_path: str, output_path: str, replacements: Dict[str, str]
) -> str:
    """[Experimental] 기존 HWP 파일의 문자열을 일괄 치환해 별도 파일로 저장합니다.

    원본 파일을 변경하지 않습니다. 표 셀 전용 API와 자동 롤백은 아직 지원하지 않습니다.
    Windows/한글 실사용 검증은 별도 진행 중입니다.
    """
    try:
        from hwp_unified.worker import invoke_hwp_worker

        result = invoke_hwp_worker(
            "replace", source=input_path, destination=output_path,
            replacements=replacements
        )
        return f"새 HWP 파일을 저장했습니다: {result} (문서 내용 실기 재확인 권장)"
    except Exception as exc:
        logger.error("HWP 일괄 치환 실패: %s", exc)
        return f"HWP 일괄 치환 실패: {exc}"


def convert_pdf_to_html(
    pdf_path: str, output_dir: str, mode: str = "editable"
) -> str:
    """[Experimental] 텍스트 기반 PDF를 HTML로 변환합니다.

    mode=editable 또는 faithful. OCR·표·이미지 정밀 재현은 미지원입니다.
    """
    try:
        from hwp_unified.conversion import pdf_to_html

        result = pdf_to_html(pdf_path, output_dir, mode)
        return f"PDF 텍스트 HTML 생성 완료: {result} (표/이미지/서식 보존은 미지원)"
    except Exception as exc:
        logger.error("PDF→HTML 변환 실패: %s", exc)
        return f"PDF→HTML 변환 실패: {exc}"


def convert_hwp_to_html(
    hwp_path: str, output_dir: str, mode: str = "editable"
) -> str:
    """[Experimental] 별도 한글 인스턴스에서 HWP→PDF→텍스트 HTML로 변환합니다.

    Windows/한글/PyMuPDF 필요. 원본 보존·출력 덮어쓰기 금지.
    """
    try:
        from hwp_unified.worker import invoke_hwp_worker

        result = invoke_hwp_worker(
            "hwp_to_html", source=hwp_path, output_dir=output_dir, mode=mode
        )
        return f"HWP 텍스트 HTML 생성 완료: {result} (실제 HWP/레이아웃 재검증 필요)"
    except Exception as exc:
        logger.error("HWP→HTML 변환 실패: %s", exc)
        return f"HWP→HTML 변환 실패: {exc}"


# Real Windows/Hangul integration is not yet reliable. Experimental tools
# must be explicitly enabled; default tool discovery remains unchanged.
if os.environ.get("HWP_MCP_ENABLE_EXPERIMENTAL") == "1":
    mcp.tool()(replace_document_text)
    mcp.tool()(convert_pdf_to_html)
    mcp.tool()(convert_hwp_to_html)


def main():
    """메인 함수"""
    try:
        logger.info("Advanced HWP MCP Server 시작")
        
        # 연결만으로 한글을 실행하지 않는다.
        # 실제 도구가 호출되면 check_initialization()에서 지연 초기화한다.
        # MCP 서버 실행
        mcp.run()
        
    except Exception as e:
        logger.error(f"서버 실행 중 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()