"""
SourceAnalyzer 해시값 생성 및 변경감지 공통 유틸리티 모듈
- 해시값 생성 (MD5, SHA256)
- 파일 해시 생성 및 변경감지
- 내용 해시 생성
"""

import hashlib
import os
from typing import Optional
from .logger import app_logger, handle_error


class HashUtils:
    """해시값 생성 및 변경감지 관련 공통 유틸리티 클래스"""
    
    @staticmethod
    def generate_md5(content: str) -> str:
        """
        MD5 해시값 생성
        
        Args:
            content: 해시를 생성할 문자열
            
        Returns:
            MD5 해시값 (32자리 16진수 문자열)
        """
        try:
            return hashlib.md5(content.encode('utf-8')).hexdigest()
        except Exception as e:
            handle_error(e, f"MD5 해시 생성 실패")
            return ""
    
    @staticmethod
    def generate_sha256(content: str) -> str:
        """
        SHA256 해시값 생성
        
        Args:
            content: 해시를 생성할 문자열
            
        Returns:
            SHA256 해시값 (64자리 16진수 문자열)
        """
        try:
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
        except Exception as e:
            handle_error(e, f"SHA256 해시 생성 실패")
            return ""
    
    @staticmethod
    def generate_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """
        파일 내용의 해시값을 계산
        
        Args:
            file_path: 파일 경로
            algorithm: 해시 알고리즘 ('md5' 또는 'sha256')
            
        Returns:
            해시값 (문자열) 또는 None (실패시)
        """
        try:
            if not os.path.exists(file_path):
                app_logger.warning(f"파일이 존재하지 않습니다: {file_path}")
                return None
            
            if algorithm == 'md5':
                hash_obj = hashlib.md5()
            elif algorithm == 'sha256':
                hash_obj = hashlib.sha256()
            else:
                app_logger.warning(f"지원하지 않는 해시 알고리즘: {algorithm}")
                return None
            
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            hash_value = hash_obj.hexdigest()
            app_logger.debug(f"파일 해시 생성 성공: {file_path} ({algorithm})")
            return hash_value
            
        except Exception as e:
            handle_error(e, f"파일 해시 계산 실패: {file_path}")
            return None
    
    @staticmethod
    def is_file_changed(file_path: str, previous_hash: str, algorithm: str = 'md5') -> bool:
        """
        파일이 변경되었는지 확인
        
        Args:
            file_path: 파일 경로
            previous_hash: 이전 해시값
            algorithm: 해시 알고리즘 ('md5' 또는 'sha256')
            
        Returns:
            파일 변경 여부 (True: 변경됨, False: 변경되지 않음)
        """
        try:
            current_hash = HashUtils.generate_file_hash(file_path, algorithm)
            
            if current_hash is None:
                app_logger.warning(f"파일 해시 생성 실패, 변경됨으로 간주: {file_path}")
                return True
            
            is_changed = current_hash != previous_hash
            
            if is_changed:
                app_logger.debug(f"파일 변경 감지: {file_path}")
            else:
                app_logger.debug(f"파일 변경 없음: {file_path}")
            
            return is_changed
            
        except Exception as e:
            handle_error(e, f"파일 변경 확인 실패: {file_path}")
            return True  # 오류 시 변경됨으로 간주
    
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
        try:
            if algorithm == 'md5':
                return hashlib.md5(content.encode('utf-8')).hexdigest()
            elif algorithm == 'sha256':
                return hashlib.sha256(content.encode('utf-8')).hexdigest()
            else:
                app_logger.warning(f"지원하지 않는 해시 알고리즘: {algorithm}, MD5로 대체")
                return hashlib.md5(content.encode('utf-8')).hexdigest()
                
        except Exception as e:
            handle_error(e, f"내용 해시 계산 실패")
            return ""


# 편의 함수들
def generate_md5(content: str) -> str:
    """MD5 해시 생성 편의 함수"""
    return HashUtils.generate_md5(content)


def generate_sha256(content: str) -> str:
    """SHA256 해시 생성 편의 함수"""
    return HashUtils.generate_sha256(content)


def generate_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
    """파일 해시 생성 편의 함수"""
    return HashUtils.generate_file_hash(file_path, algorithm)
