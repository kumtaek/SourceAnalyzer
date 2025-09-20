"""
SourceAnalyzer 경로 처리 공통 유틸리티 모듈
- 크로스플랫폼 경로 처리
- 프로젝트 경로 관리
- 경로 유효성 검사
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from .logger import app_logger, handle_error


class PathUtils:
    """경로 처리 관련 공통 유틸리티 클래스"""
    
    def __init__(self, project_root: str = None):
        """
        경로 유틸리티 초기화
        
        Args:
            project_root: 프로젝트 루트 경로 (기본값: 현재 작업 디렉토리)
        """
        if project_root is None:
            # 현재 스크립트가 실행되는 디렉토리를 프로젝트 루트로 설정
            # util 폴더의 상위 디렉토리가 프로젝트 루트
            current_file = os.path.abspath(__file__)
            util_dir = os.path.dirname(current_file)
            self.project_root = os.path.dirname(util_dir)  # util의 상위 디렉토리
        else:
            self.project_root = os.path.abspath(project_root)
    
    def normalize_path(self, path: str) -> str:
        """
        경로 정규화 (절대경로로 변환)
        
        Args:
            path: 정규화할 경로
            
        Returns:
            정규화된 절대경로
        """
        try:
            if not path:
                return ""
            
            # 절대경로인 경우 그대로 정규화
            if os.path.isabs(path):
                return os.path.normpath(path)
            
            # 상대경로인 경우 프로젝트 루트 기준으로 변환
            return os.path.normpath(os.path.join(self.project_root, path))
            
        except Exception as e:
            handle_error(e, f"경로 정규화 실패: {path}")
            return path
    
    def get_relative_path(self, target_path: str, base_path: str = None) -> str:
        """
        상대경로 생성
        
        Args:
            target_path: 대상 경로
            base_path: 기준 경로 (기본값: 프로젝트 루트)
            
        Returns:
            상대경로
        """
        try:
            if not target_path:
                return ""
            
            if base_path is None:
                base_path = self.project_root
            
            # 경로 정규화
            target_abs = self.normalize_path(target_path)
            base_abs = self.normalize_path(base_path)
            
            # 상대경로 생성
            relative_path = os.path.relpath(target_abs, base_abs)
            
            # Windows에서 상대경로가 상위 디렉토리로 나가는 경우 처리
            if relative_path.startswith('..'):
                handle_error(Exception(f"상대경로가 프로젝트 루트를 벗어남: {target_path}"), f"경로 오류: {target_path}")
            
            return relative_path
            
        except ValueError:
            # 다른 드라이브에 있는 경우 절대경로 반환
            handle_error(Exception(f"다른 드라이브 경로: {target_path}"), f"경로 오류: {target_path}")
        except Exception as e:
            handle_error(e, f"상대경로 생성 실패: {target_path}")
            return target_path
    
    def get_absolute_path(self, path: str) -> str:
        """
        절대경로 반환
        
        Args:
            path: 경로
            
        Returns:
            절대경로
        """
        try:
            return os.path.abspath(path)
        except Exception as e:
            handle_error(e, f"절대경로 생성 실패: {path}")
            return path
    
    def join_path(self, *args) -> str:
        """
        경로 결합 (크로스플랫폼 지원)
        
        Args:
            *args: 결합할 경로 요소들
            
        Returns:
            결합된 경로
        """
        try:
            return os.path.join(*args)
        except Exception as e:
            handle_error(e, f"경로 결합 실패: {args}")
            return os.path.join(*args)
    
    def get_filename(self, path: str) -> str:
        """
        파일 이름 추출
        
        Args:
            path: 파일 경로
            
        Returns:
            파일 이름
        """
        try:
            return os.path.basename(path)
        except Exception as e:
            handle_error(e, f"파일 이름 추출 실패: {path}")
            return path
    
    def get_dirname(self, path: str) -> str:
        """
        디렉토리 이름 추출
        
        Args:
            path: 파일 또는 디렉토리 경로
            
        Returns:
            디렉토리 이름
        """
        try:
            return os.path.dirname(path)
        except Exception as e:
            handle_error(e, f"디렉토리 이름 추출 실패: {path}")
            return path
    
    def get_extension(self, path: str) -> str:
        """
        파일 확장자 추출
        
        Args:
            path: 파일 경로
            
        Returns:
            파일 확장자 (예: .py, .java)
        """
        try:
            return Path(path).suffix
        except Exception as e:
            handle_error(e, f"파일 확장자 추출 실패: {path}")
            return ""
    
    def get_file_stem(self, path: str) -> str:
        """
        파일 이름에서 확장자를 제외한 부분 추출
        
        Args:
            path: 파일 경로
            
        Returns:
            파일 이름 (확장자 제외)
        """
        try:
            return Path(path).stem
        except Exception as e:
            handle_error(e, f"파일 스템 추출 실패: {path}")
            return path
    
    def exists(self, path: str) -> bool:
        """
        경로 존재 여부 확인
        
        Args:
            path: 확인할 경로
            
        Returns:
            존재 여부
        """
        try:
            return os.path.exists(path)
        except Exception as e:
            handle_error(e, f"경로 존재 여부 확인 실패: {path}")
            return False
    
    def is_file(self, path: str) -> bool:
        """
        파일 여부 확인
        
        Args:
            path: 확인할 경로
            
        Returns:
            파일 여부
        """
        try:
            return os.path.isfile(path)
        except Exception as e:
            handle_error(e, f"파일 여부 확인 실패: {path}")
            return False
    
    def is_dir(self, path: str) -> bool:
        """
        디렉토리 여부 확인
        
        Args:
            path: 확인할 경로
            
        Returns:
            디렉토리 여부
        """
        try:
            return os.path.isdir(path)
        except Exception as e:
            handle_error(e, f"디렉토리 여부 확인 실패: {path}")
            return False
    
    def list_files(self, directory: str, pattern: str = "*") -> List[str]:
        """
        디렉토리 내 파일 목록 조회 (패턴 매칭)
        
        Args:
            directory: 조회할 디렉토리
            pattern: 파일 패턴 (예: *.java)
            
        Returns:
            파일 경로 리스트
        """
        try:
            return [str(p) for p in Path(directory).glob(pattern) if p.is_file()]
        except Exception as e:
            handle_error(e, f"파일 목록 조회 실패: {directory}")
            return []
    
    def list_dirs(self, directory: str, pattern: str = "*") -> List[str]:
        """
        디렉토리 내 서브 디렉토리 목록 조회 (패턴 매칭)
        
        Args:
            directory: 조회할 디렉토리
            pattern: 디렉토리 패턴
            
        Returns:
            디렉토리 경로 리스트
        """
        try:
            return [str(p) for p in Path(directory).glob(pattern) if p.is_dir()]
        except Exception as e:
            handle_error(e, f"디렉토리 목록 조회 실패: {directory}")
            return []
    
    def get_project_relative_path(self, absolute_path: str) -> str:
        """
        프로젝트 루트를 기준으로 한 상대 경로 반환
        
        Args:
            absolute_path: 절대 경로
            
        Returns:
            프로젝트 루트 기준 상대 경로
        """
        try:
            return os.path.relpath(absolute_path, self.project_root)
        except ValueError:
            # 다른 드라이브에 있는 경우 절대경로 반환
            return absolute_path
        except Exception as e:
            handle_error(e, f"프로젝트 상대 경로 생성 실패: {absolute_path}")
            return absolute_path
    
    def get_project_root(self) -> str:
        """프로젝트 루트 경로 반환"""
        return self.project_root


# 프로젝트 경로 관련 편의 함수들
def get_project_source_path(project_name: str) -> str:
    """프로젝트 소스 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("projects", project_name, "src")


def get_project_config_path(project_name: str) -> str:
    """프로젝트 설정 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("projects", project_name, "config")


def get_project_db_schema_path(project_name: str) -> str:
    """프로젝트 DB 스키마 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("projects", project_name, "db_schema")


def get_project_report_path(project_name: str) -> str:
    """프로젝트 리포트 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("projects", project_name, "Report")


def get_project_metadata_db_path(project_name: str) -> str:
    """프로젝트 메타데이터 DB 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("projects", project_name, f"{project_name}_metadata.db")


def get_config_path() -> str:
    """설정 파일 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("config")


def get_database_schema_path() -> str:
    """데이터베이스 스키마 파일 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("database", "create_table_script.sql")


def get_parser_config_path() -> str:
    """파서 설정 파일 경로 반환"""
    path_utils = PathUtils()
    return path_utils.join_path("config", "parser")


def list_projects() -> List[str]:
    """프로젝트 목록 조회"""
    try:
        path_utils = PathUtils()
        projects_dir = path_utils.join_path("projects")
        
        if not path_utils.exists(projects_dir):
            return []
        
        project_dirs = path_utils.list_dirs(projects_dir)
        project_names = [path_utils.get_filename(project_dir) for project_dir in project_dirs]
        
        return project_names
        
    except Exception as e:
        handle_error(e, f"프로젝트 목록 조회 실패")
        return []


def project_exists(project_name: str) -> bool:
    """프로젝트 존재 여부 확인"""
    try:
        path_utils = PathUtils()
        project_path = path_utils.join_path("projects", project_name)
        return path_utils.exists(project_path) and path_utils.is_dir(project_path)
        
    except Exception as e:
        handle_error(e, f"프로젝트 존재 여부 확인 실패: {project_name}")
        return False


# 편의 함수들
def normalize_path(path: str) -> str:
    """경로 정규화 편의 함수"""
    path_utils = PathUtils()
    return path_utils.normalize_path(path)


def get_relative_path(target_path: str, base_path: str = None) -> str:
    """상대경로 생성 편의 함수"""
    path_utils = PathUtils()
    return path_utils.get_relative_path(target_path, base_path)


def get_absolute_path(path: str) -> str:
    """절대경로 반환 편의 함수"""
    path_utils = PathUtils()
    return path_utils.get_absolute_path(path)


def join_path(*args) -> str:
    """경로 결합 편의 함수"""
    path_utils = PathUtils()
    return path_utils.join_path(*args)
