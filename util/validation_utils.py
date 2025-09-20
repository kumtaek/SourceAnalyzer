"""
SourceAnalyzer 유효성 검사 공통 유틸리티 모듈
- 프로젝트명 유효성 검사
- 파일 경로 유효성 검사
- 필수 필드 검증
"""

import os
import re
from typing import Any, Dict, List, Optional, Union
from .logger import app_logger, handle_error
from .path_utils import PathUtils


class ValidationUtils:
    """유효성 검사 관련 공통 유틸리티 클래스"""
    
    # 유효성 검사 패턴
    VALID_PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
    VALID_FILE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')
    
    @staticmethod
    def is_valid_project_name(project_name: str) -> bool:
        """
        프로젝트명 유효성 검사
        
        Args:
            project_name: 검사할 프로젝트명
            
        Returns:
            유효성 검사 통과 여부
        """
        try:
            if not project_name or not isinstance(project_name, str):
                return False
            
            # 길이 검사
            if len(project_name) < 1 or len(project_name) > 50:
                return False
            
            # 패턴 검사
            if not ValidationUtils.VALID_PROJECT_NAME_PATTERN.match(project_name):
                return False
            
            # 예약어 검사
            reserved_names = ['config', 'temp', 'logs', 'database', 'util', 'parser', 'reports']
            if project_name.lower() in reserved_names:
                return False
            
            return True
            
        except Exception as e:
            handle_error(e, f"프로젝트명 유효성 검사 실패: {project_name}")
            return False
    
    @staticmethod
    def is_valid_file_path(file_path: str) -> bool:
        """
        파일 경로 유효성 검사
        
        Args:
            file_path: 검사할 파일 경로
            
        Returns:
            유효성 검사 통과 여부
        """
        try:
            if not file_path or not isinstance(file_path, str):
                return False
            
            # 길이 검사
            if len(file_path) > 260:  # Windows 경로 길이 제한
                return False
            
            # 금지된 문자 검사
            forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']
            for char in forbidden_chars:
                if char in file_path:
                    return False
            
            # 경로 정규화 테스트
            try:
                os.path.normpath(file_path)
            except (OSError, ValueError):
                return False
            
            return True
            
        except Exception as e:
            handle_error(e, f"파일 경로 유효성 검사 실패: {file_path}")
            return False
    
    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """
        파일 존재 여부 검증
        
        Args:
            file_path: 검사할 파일 경로
            
        Returns:
            파일 존재 여부
        """
        try:
            if not ValidationUtils.is_valid_file_path(file_path):
                return False
            
            return os.path.exists(file_path) and os.path.isfile(file_path)
            
        except Exception as e:
            handle_error(e, f"파일 존재 여부 검증 실패: {file_path}")
            return False
    
    @staticmethod
    def validate_directory_exists(directory_path: str) -> bool:
        """
        디렉토리 존재 여부 검증
        
        Args:
            directory_path: 검사할 디렉토리 경로
            
        Returns:
            디렉토리 존재 여부
        """
        try:
            if not ValidationUtils.is_valid_file_path(directory_path):
                return False
            
            return os.path.exists(directory_path) and os.path.isdir(directory_path)
            
        except Exception as e:
            handle_error(e, f"디렉토리 존재 여부 검증 실패: {directory_path}")
            return False
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """
        필수 필드 검증
        
        Args:
            data: 검증할 데이터 딕셔너리
            required_fields: 필수 필드 목록
            
        Returns:
            검증 결과 딕셔너리
        """
        try:
            result = {
                'is_valid': True,
                'missing_fields': [],
                'errors': []
            }
            
            for field in required_fields:
                if field not in data or data[field] is None or data[field] == '':
                    result['missing_fields'].append(field)
                    result['is_valid'] = False
            
            if not result['is_valid']:
                error_msg = f"필수 필드 누락: {result['missing_fields']}"
                result['errors'].append(error_msg)
                app_logger.warning(error_msg)
            
            return result
            
        except Exception as e:
            handle_error(e, f"필수 필드 검증 실패")
            return {
                'is_valid': False,
                'missing_fields': [],
                'errors': [f"검증 오류: {str(e)}"]
            }
    
    @staticmethod
    def validate_file_extension(file_path: str, allowed_extensions: List[str]) -> bool:
        """
        파일 확장자 검증
        
        Args:
            file_path: 검사할 파일 경로
            allowed_extensions: 허용된 확장자 목록
            
        Returns:
            확장자 유효성 검사 통과 여부
        """
        try:
            if not ValidationUtils.is_valid_file_path(file_path):
                return False
            
            file_extension = os.path.splitext(file_path)[1].lower()
            return file_extension in allowed_extensions
            
        except Exception as e:
            handle_error(e, f"파일 확장자 검증 실패: {file_path}")
            return False
    
    @staticmethod
    def validate_project_structure(project_name: str) -> Dict[str, Any]:
        """
        프로젝트 구조 검증
        
        Args:
            project_name: 검사할 프로젝트명
            
        Returns:
            프로젝트 구조 검증 결과
        """
        try:
            path_utils = PathUtils()
            result = {
                'is_valid': True,
                'missing_directories': [],
                'missing_files': [],
                'errors': []
            }
            
            # 프로젝트명 유효성 검사
            if not ValidationUtils.is_valid_project_name(project_name):
                result['is_valid'] = False
                result['errors'].append(f"유효하지 않은 프로젝트명: {project_name}")
                return result
            
            # 필수 디렉토리 검사
            required_dirs = [
                path_utils.join_path("projects", project_name, "src"),
                path_utils.join_path("projects", project_name, "config"),
                path_utils.join_path("projects", project_name, "db_schema")
            ]
            
            for dir_path in required_dirs:
                if not ValidationUtils.validate_directory_exists(dir_path):
                    result['missing_directories'].append(dir_path)
                    result['is_valid'] = False
            
            # 필수 파일 검사
            required_files = [
                path_utils.join_path("projects", project_name, "config", "target_source_config.yaml"),
                path_utils.join_path("projects", project_name, "db_schema", "ALL_TABLES.csv"),
                path_utils.join_path("projects", project_name, "db_schema", "ALL_TAB_COLUMNS.csv")
            ]
            
            for file_path in required_files:
                if not ValidationUtils.validate_file_exists(file_path):
                    result['missing_files'].append(file_path)
                    result['is_valid'] = False
            
            if not result['is_valid']:
                error_msg = f"프로젝트 구조 검증 실패: {project_name}"
                if result['missing_directories']:
                    error_msg += f"\n누락된 디렉토리: {result['missing_directories']}"
                if result['missing_files']:
                    error_msg += f"\n누락된 파일: {result['missing_files']}"
                result['errors'].append(error_msg)
                app_logger.warning(error_msg)
            
            return result
            
        except Exception as e:
            handle_error(e, f"프로젝트 구조 검증 실패: {project_name}")
            return {
                'is_valid': False,
                'missing_directories': [],
                'missing_files': [],
                'errors': [f"검증 오류: {str(e)}"]
            }


# 편의 함수들
def is_valid_project_name(project_name: str) -> bool:
    """프로젝트명 유효성 검사 편의 함수"""
    return ValidationUtils.is_valid_project_name(project_name)


def is_valid_file_path(file_path: str) -> bool:
    """파일 경로 유효성 검사 편의 함수"""
    return ValidationUtils.is_valid_file_path(file_path)


def validate_file_exists(file_path: str) -> bool:
    """파일 존재 여부 검증 편의 함수"""
    return ValidationUtils.validate_file_exists(file_path)
