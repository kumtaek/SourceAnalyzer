"""
SourceAnalyzer 파일 처리 공통 유틸리티 모듈
- 다중 인코딩 지원 파일 읽기/쓰기
- 파일 타입 감지
- 파일 해시값 생성
"""

import os
import mimetypes
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from .logger import app_logger, handle_error, info, debug
from .hash_utils import HashUtils


class FileUtils:
    """파일 처리 관련 공통 유틸리티 클래스"""
    
    # 지원하는 파일 타입 정의
    SUPPORTED_EXTENSIONS = {
        'java': ['.java'],
        'xml': ['.xml'],
        'jsp': ['.jsp'],
        'sql': ['.sql'],
        'csv': ['.csv'],
        'yaml': ['.yaml', '.yml'],
        'properties': ['.properties'],
        'txt': ['.txt'],
        'json': ['.json'],
        'vue': ['.vue'],
        'jsx': ['.jsx'],
        'tsx': ['.tsx'],
        'js': ['.js'],
        'ts': ['.ts'],
        'html': ['.html', '.htm'],
        'css': ['.css'],
        'scss': ['.scss'],
        'sass': ['.sass']
    }
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        파일을 읽어서 내용을 반환 (다중 인코딩 지원)
        
        Args:
            file_path: 읽을 파일 경로
            encoding: 파일 인코딩 (기본값: utf-8)
            
        Returns:
            파일 내용 (문자열) 또는 None (읽기 실패시)
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                app_logger.debug(f"파일 읽기 성공: {file_path}")
                return content
        except FileNotFoundError:
            handle_error(Exception(f"파일을 찾을 수 없습니다: {file_path}"), f"파일 읽기 실패: {file_path}")
        except UnicodeDecodeError:
            filename = os.path.basename(file_path)
            info(f"인코딩 문제 감지, 다른 인코딩으로 재시도: {filename}")
            
            # UTF-8 BOM 처리 시도
            try:
                with open(file_path, 'r', encoding='utf-8-sig') as file:
                    content = file.read()
                    app_logger.debug(f"파일 읽기 성공 (utf-8-sig): {file_path}")
                    return content
            except UnicodeDecodeError:
                # UTF-8 BOM 실패하면 CP949 시도
                try:
                    with open(file_path, 'r', encoding='cp949') as file:
                        content = file.read()
                        app_logger.debug(f"파일 읽기 성공 (cp949): {file_path}")
                        return content
                except UnicodeDecodeError:
                    # CP949도 실패하면 EUC-KR 시도
                    try:
                        with open(file_path, 'r', encoding='euc-kr') as file:
                            content = file.read()
                            app_logger.debug(f"파일 읽기 성공 (euc-kr): {file_path}")
                            return content
                    except UnicodeDecodeError:
                        # 모든 인코딩 실패 시 에러 처리
                        handle_error(Exception(f"모든 인코딩 시도 실패 (utf-8, utf-8-sig, cp949, euc-kr): {file_path}"), f"파일 인코딩 문제: {file_path}")
                        return None
                except Exception as e:
                    handle_error(e, f"파일 읽기 실패: {file_path}")
                    return None
            except Exception as e:
                handle_error(e, f"파일 읽기 실패: {file_path}")
                return None
        except Exception as e:
            handle_error(e, f"파일 읽기 실패: {file_path}")
            return None
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """
        파일에 내용을 쓴다
        
        Args:
            file_path: 쓸 파일 경로
            content: 쓸 내용
            encoding: 파일 인코딩 (기본값: utf-8)
            
        Returns:
            쓰기 성공 여부
        """
        try:
            # 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(content)
            
            app_logger.debug(f"파일 쓰기 성공: {file_path}")
            return True
            
        except Exception as e:
            handle_error(e, f"파일 쓰기 실패: {file_path}")
            return False
    
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """
        파일 타입 감지
        
        Args:
            file_path: 파일 경로
            
        Returns:
            파일 타입 (확장자 기반)
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            # 지원하는 파일 타입 확인
            for file_type, extensions in FileUtils.SUPPORTED_EXTENSIONS.items():
                if file_extension in extensions:
                    return file_type
            
            # MIME 타입으로 추가 확인
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                return mime_type.split('/')[0]  # text, application 등
            
            return 'unknown'
            
        except Exception as e:
            handle_error(e, f"파일 타입 감지 실패: {file_path}")
            return 'unknown'
    
    @staticmethod
    def get_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """
        파일 내용의 해시값을 계산
        
        Args:
            file_path: 파일 경로
            algorithm: 해시 알고리즘 ('md5' 또는 'sha256')
            
        Returns:
            해시값 (문자열) 또는 None (실패시)
        """
        return HashUtils.generate_file_hash(file_path, algorithm)
    
    @staticmethod
    def get_content_hash(content: str, algorithm: str = 'md5') -> str:
        """
        문자열 내용의 해시값을 계산
        
        Args:
            content: 해시를 계산할 문자열
            algorithm: 해시 알고리즘 ('md5' 또는 'sha256')
            
        Returns:
            해시값 (문자열)
        """
        return HashUtils.get_content_hash(content, algorithm)
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        파일 정보 조회
        
        Args:
            file_path: 파일 경로
            
        Returns:
            파일 정보 딕셔너리
        """
        try:
            if not os.path.exists(file_path):
                return {
                    'exists': False,
                    'error': '파일이 존재하지 않습니다'
                }
            
            stat_info = os.stat(file_path)
            
            return {
                'exists': True,
                'size': stat_info.st_size,
                'modified_time': time.ctime(stat_info.st_mtime),
                'created_time': time.ctime(stat_info.st_ctime),
                'extension': Path(file_path).suffix,
                'file_type': FileUtils.get_file_type(file_path),
                'hash_md5': FileUtils.get_file_hash(file_path, 'md5'),
                'hash_sha256': FileUtils.get_file_hash(file_path, 'sha256')
            }
            
        except Exception as e:
            handle_error(e, f"파일 정보 조회 실패: {file_path}")
            return {
                'exists': False,
                'error': str(e)
            }
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*", recursive: bool = True) -> List[str]:
        """
        디렉토리 내 파일 목록 조회
        
        Args:
            directory: 조회할 디렉토리
            pattern: 파일 패턴 (예: *.java)
            recursive: 재귀 검색 여부
            
        Returns:
            파일 경로 리스트
        """
        try:
            if not os.path.exists(directory):
                app_logger.warning(f"디렉토리가 존재하지 않습니다: {directory}")
                return []
            
            path_obj = Path(directory)
            
            if recursive:
                files = list(path_obj.rglob(pattern))
            else:
                files = list(path_obj.glob(pattern))
            
            # 파일만 필터링
            file_paths = [str(f) for f in files if f.is_file()]
            
            app_logger.debug(f"파일 목록 조회 완료: {directory}, 파일 수: {len(file_paths)}")
            return file_paths
            
        except Exception as e:
            handle_error(e, f"파일 목록 조회 실패: {directory}")
            return []
    
    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """
        지원하는 파일 타입인지 확인
        
        Args:
            file_path: 파일 경로
            
        Returns:
            지원 여부
        """
        try:
            file_type = FileUtils.get_file_type(file_path)
            return file_type != 'unknown'
            
        except Exception as e:
            handle_error(e, f"파일 지원 여부 확인 실패: {file_path}")
            return False


# 편의 함수들
def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """파일 읽기 편의 함수"""
    return FileUtils.read_file(file_path, encoding)


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """파일 쓰기 편의 함수"""
    return FileUtils.write_file(file_path, content, encoding)


def get_file_type(file_path: str) -> str:
    """파일 타입 감지 편의 함수"""
    return FileUtils.get_file_type(file_path)


def get_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
    """파일 해시 생성 편의 함수"""
    return FileUtils.get_file_hash(file_path, algorithm)


def get_content_hash(content: str, algorithm: str = 'md5') -> str:
    """내용 해시 생성 편의 함수"""
    return FileUtils.get_content_hash(content, algorithm)
