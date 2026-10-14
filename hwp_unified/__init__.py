"""Opt-in HWP workflow and document conversion modules.

These functions do not start Hangul or import COM until explicitly invoked.
Windows/Hangul real-world acceptance remains separate from mock tests.
"""
from .workflow import HwpWorkflowError, run_replace_job
from .conversion import ConversionError, pdf_to_html, hwp_to_html

__all__ = ["HwpWorkflowError", "run_replace_job", "ConversionError", "pdf_to_html", "hwp_to_html"]
