"""
Paper Review System - Modules Package
论文评审系统模块包
"""

__version__ = "0.1.0"

from .pdf_parser import parse_pdf_to_markdown, get_markdown_preview
from .metadata_extractor import extract_metadata, extract_detailed_sections
from .format_validator import validate_paper_format, print_validation_report

__all__ = [
    'parse_pdf_to_markdown',
    'get_markdown_preview',
    'extract_metadata',
    'extract_detailed_sections',
    'validate_paper_format',
    'print_validation_report',
]
