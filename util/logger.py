"""
SourceAnalyzer 로깅 시스템 공통 유틸리티 모듈
- 중앙 집중식 로깅 관리
- 파일명:라인번호 포함 로그 포맷
- 전역 handle_error 함수
"""

import logging
import logging.config
import sys
import traceback
import os
from datetime import datetime
from typing import Optional
import yaml


class SourceAnalyzerLogger:
    """SourceAnalyzer 전용 로거 클래스"""
    
    def __init__(self, logger_name: str = "SourceAnalyzer"):
        """
        Args:
            logger_name: 로거 이름
        """
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.log_file_path = self._get_log_file_path()
        self._setup_logger()
    
    def _get_log_file_path(self) -> str:
        """로그 파일 경로 생성"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"logs/SourceAnalyzer_{timestamp}.log"
    
    def _setup_logger(self):
        """로거 설정 - 중앙 집중식 설정 파일 사용"""
        try:
            # 로깅 설정 파일 로드
            config_path = os.path.join("config", "logging.yaml")
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                # 로그 디렉토리 생성
                os.makedirs("logs", exist_ok=True)
                
                # 로깅 설정 적용
                logging.config.dictConfig(config)
                
                # SourceAnalyzer 전용 로거 가져오기
                self.logger = logging.getLogger('SourceAnalyzer')
                
                # 파일 핸들러에 타임스탬프가 포함된 파일명 설정
                for handler in self.logger.handlers:
                    if isinstance(handler, logging.FileHandler):
                        self.logger.removeHandler(handler)
                
                # 새로운 파일 핸들러 추가
                new_file_handler = logging.FileHandler(
                    self.log_file_path,
                    encoding='utf-8'
                )
                new_file_handler.setLevel(logging.INFO)
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
                )
                new_file_handler.setFormatter(formatter)
                self.logger.addHandler(new_file_handler)
                
                self.logger.setLevel(logging.INFO)
                
            else:
                self._setup_default_logger()
                
        except Exception as e:
            print(f"로깅 시스템 초기화 실패: {e}")
            print("FATAL: 로깅 시스템 초기화 실패로 프로그램을 종료합니다.")
            sys.exit(1)
    
    def _setup_default_logger(self):
        """기본 로거 설정 (fallback)"""
        if not self.logger.handlers:
            # 로그 디렉토리 생성
            os.makedirs("logs", exist_ok=True)
            
            # 콘솔 핸들러
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # 파일 핸들러
            file_handler = logging.FileHandler(
                self.log_file_path,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            
            # 포맷터 (파일명.라인번호 포함)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)
    
    def debug(self, message: str) -> None:
        """DEBUG 레벨 로그"""
        try:
            self.logger.debug(message, stacklevel=2)
        except RecursionError:
            print(f"[DEBUG] {message}")
    
    def info(self, message: str) -> None:
        """INFO 레벨 로그"""
        try:
            self.logger.info(message, stacklevel=2)
        except RecursionError:
            print(f"[INFO] {message}")
    
    def warning(self, message: str) -> None:
        """WARNING 레벨 로그"""
        try:
            self.logger.warning(message, stacklevel=2)
        except RecursionError:
            print(f"[WARNING] {message}")
    
    def error(self, message: str) -> None:
        """ERROR 레벨 로그"""
        try:
            self.logger.error(message, stacklevel=2)
        except RecursionError:
            print(f"[ERROR] {message}")
    
    def critical(self, message: str) -> None:
        """CRITICAL 레벨 로그"""
        try:
            self.logger.critical(message, stacklevel=2)
        except RecursionError:
            print(f"[CRITICAL] {message}")
    
    def get_log_file_path(self) -> str:
        """현재 로그 파일 경로 반환"""
        return self.log_file_path
    
    def handle_error(self, 
                    error: Exception, 
                    custom_message: Optional[str] = None,
                    exit_code: int = 1) -> None:
        """
        에러 로그 기록 후 프로그램 종료
        
        Args:
            error: 발생한 Exception
            custom_message: 추가 메시지
            exit_code: 종료 코드 (기본값: 1)
        """
        # 스택 트레이스에서 라인번호 추출
        try:
            tb = traceback.extract_tb(error.__traceback__)
        except RecursionError:
            self.logger.error(f"[ERROR] RecursionError in traceback processing")
            tb = None
            
        if tb:
            # 가장 최근 프레임 (에러 발생 위치)
            frame = tb[-1]
            filename = frame.filename
            line_number = frame.lineno
            function_name = frame.name
            code_line = frame.line
            
            # 에러 메시지 구성
            error_msg = f"FATAL ERROR at {filename}:{line_number} in {function_name}()"
            if code_line:
                error_msg += f"\nCode: {code_line.strip()}"
            
            if custom_message:
                error_msg += f"\nMessage: {custom_message}"
            
            error_msg += f"\nException: {type(error).__name__}: {str(error)}"
            
            # 스택 트레이스 추가
            error_msg += f"\nStack Trace:\n{traceback.format_exc()}"
            
        else:
            # 스택 트레이스가 없는 경우
            error_msg = f"FATAL ERROR: {type(error).__name__}: {str(error)}"
            if custom_message:
                error_msg += f"\nMessage: {custom_message}"
        
        # 에러 로그 기록
        self.logger.error(error_msg)
        
        # 프로그램 종료
        self.logger.error(f"\n[FATAL ERROR] 프로그램이 에러로 인해 종료됩니다. (종료코드: {exit_code})")
        self.logger.error(f"자세한 내용은 로그 파일을 확인하세요: {self.log_file_path}")
        sys.exit(exit_code)


# 전역 로거 인스턴스
app_logger = SourceAnalyzerLogger()


# 편의 함수들
def debug(message: str) -> None:
    """DEBUG 로그 편의 함수"""
    try:
        app_logger.logger.debug(message, stacklevel=2)
    except RecursionError:
        print(f"[DEBUG] {message}")


def info(message: str) -> None:
    """INFO 로그 편의 함수"""
    try:
        app_logger.logger.info(message, stacklevel=2)
    except RecursionError:
        print(f"[INFO] {message}")


def warning(message: str) -> None:
    """WARNING 로그 편의 함수"""
    try:
        app_logger.logger.warning(message, stacklevel=2)
    except RecursionError:
        print(f"[WARNING] {message}")


def error(message: str) -> None:
    """ERROR 로그 편의 함수"""
    try:
        app_logger.logger.error(message, stacklevel=2)
    except RecursionError:
        print(f"[ERROR] {message}")


def critical(message: str) -> None:
    """CRITICAL 로그 편의 함수"""
    try:
        app_logger.logger.critical(message, stacklevel=2)
    except RecursionError:
        print(f"[CRITICAL] {message}")


def get_log_file_path() -> str:
    """현재 로그 파일 경로 반환"""
    return app_logger.get_log_file_path()


def handle_error(error: Exception, 
                custom_message: Optional[str] = None,
                exit_code: int = 1) -> None:
    """
    전역 에러 처리 함수 (편의 함수)
    
    Args:
        error: 발생한 Exception
        custom_message: 추가 메시지
        exit_code: 종료 코드
    """
    app_logger.handle_error(error, custom_message, exit_code)
