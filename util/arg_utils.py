"""
SourceAnalyzer 명령행 인수 처리 공통 유틸리티 모듈
- 명령행 인수 파싱
- 프로젝트명 추출 및 검증
- 사용법 출력
"""

import argparse
import sys
from typing import Optional, Dict, Any
from .logger import app_logger, handle_error
from .validation_utils import ValidationUtils


class ArgUtils:
    """명령행 인수 처리 관련 공통 유틸리티 클래스"""
    
    @staticmethod
    def create_simple_parser() -> argparse.ArgumentParser:
        """
        기본 명령행 파서 생성
        
        Returns:
            ArgumentParser 인스턴스
        """
        parser = argparse.ArgumentParser(
            description='SourceAnalyzer - 소스코드 분석 도구',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
사용 예시:
  python main.py --project-name SampleSrc --clear-metadb
  python create_report.py --project-name SampleSrc
  python main.py --project-name SampleSrc --dry-run
            """
        )
        
        # 필수 인수
        parser.add_argument(
            '--project-name',
            type=str,
            required=True,
            help='분석할 프로젝트명 (예: SampleSrc)'
        )
        
        # 선택적 인수
        parser.add_argument(
            '--clear-metadb',
            action='store_true',
            help='메타데이터베이스 초기화 후 분석'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='실제 분석 없이 검증만 수행'
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='상세 로그 출력'
        )
        
        parser.add_argument(
            '--output-dir',
            type=str,
            help='출력 디렉토리 경로 (기본값: projects/{project_name}/Report)'
        )
        
        return parser
    
    @staticmethod
    def parse_command_line_args() -> argparse.Namespace:
        """
        명령행 인수 파싱
        
        Returns:
            파싱된 인수 네임스페이스
        """
        try:
            parser = ArgUtils.create_simple_parser()
            args = parser.parse_args()
            
            app_logger.debug(f"명령행 인수 파싱 완료: {vars(args)}")
            return args
            
        except Exception as e:
            handle_error(e, f"명령행 인수 파싱 실패")
            return None
    
    @staticmethod
    def get_project_name_from_args(args: argparse.Namespace) -> Optional[str]:
        """
        파싱된 인수에서 프로젝트명 추출
        
        Args:
            args: 파싱된 인수 네임스페이스
            
        Returns:
            프로젝트명 또는 None
        """
        try:
            if not hasattr(args, 'project_name') or not args.project_name:
                app_logger.error("프로젝트명이 지정되지 않았습니다")
                return None
            
            project_name = args.project_name.strip()
            
            if not ValidationUtils.is_valid_project_name(project_name):
                app_logger.error(f"유효하지 않은 프로젝트명: {project_name}")
                return None
            
            app_logger.info(f"프로젝트명 확인: {project_name}")
            return project_name
            
        except Exception as e:
            handle_error(e, f"프로젝트명 추출 실패")
            return None
    
    @staticmethod
    def validate_and_get_project_name() -> Optional[str]:
        """
        명령행 인수에서 프로젝트명 추출 및 검증
        
        Returns:
            검증된 프로젝트명 또는 None
        """
        try:
            args = ArgUtils.parse_command_line_args()
            if not args:
                return None
            
            return ArgUtils.get_project_name_from_args(args)
            
        except Exception as e:
            handle_error(e, f"프로젝트명 검증 실패")
            return None
    
    @staticmethod
    def print_usage_and_exit(exit_code: int = 0):
        """
        사용법 출력 후 프로그램 종료
        
        Args:
            exit_code: 종료 코드
        """
        try:
            parser = ArgUtils.create_simple_parser()
            parser.print_help()
            sys.exit(exit_code)
            
        except Exception as e:
            handle_error(e, f"사용법 출력 실패")
            sys.exit(1)
    
    @staticmethod
    def get_args_dict(args: argparse.Namespace) -> Dict[str, Any]:
        """
        인수 네임스페이스를 딕셔너리로 변환
        
        Args:
            args: 파싱된 인수 네임스페이스
            
        Returns:
            인수 딕셔너리
        """
        try:
            return vars(args)
        except Exception as e:
            handle_error(e, f"인수 딕셔너리 변환 실패")
            return {}
    
    @staticmethod
    def has_flag(args: argparse.Namespace, flag_name: str) -> bool:
        """
        플래그 존재 여부 확인
        
        Args:
            args: 파싱된 인수 네임스페이스
            flag_name: 확인할 플래그명
            
        Returns:
            플래그 존재 여부
        """
        try:
            return hasattr(args, flag_name) and getattr(args, flag_name, False)
        except Exception as e:
            handle_error(e, f"플래그 확인 실패: {flag_name}")
            return False
    
    @staticmethod
    def get_option_value(args: argparse.Namespace, option_name: str, default_value: Any = None) -> Any:
        """
        옵션 값 조회
        
        Args:
            args: 파싱된 인수 네임스페이스
            option_name: 조회할 옵션명
            default_value: 기본값
            
        Returns:
            옵션 값 또는 기본값
        """
        try:
            return getattr(args, option_name, default_value)
        except Exception as e:
            handle_error(e, f"옵션 값 조회 실패: {option_name}")
            return default_value


# 편의 함수들
def parse_command_line_args() -> argparse.Namespace:
    """명령행 인수 파싱 편의 함수"""
    return ArgUtils.parse_command_line_args()


def get_project_name_from_args(args: argparse.Namespace) -> Optional[str]:
    """프로젝트명 추출 편의 함수"""
    return ArgUtils.get_project_name_from_args(args)


def validate_and_get_project_name() -> Optional[str]:
    """프로젝트명 검증 및 추출 편의 함수"""
    return ArgUtils.validate_and_get_project_name()


def create_simple_parser() -> argparse.ArgumentParser:
    """기본 파서 생성 편의 함수"""
    return ArgUtils.create_simple_parser()


def print_usage_and_exit(exit_code: int = 0):
    """사용법 출력 후 종료 편의 함수"""
    ArgUtils.print_usage_and_exit(exit_code)
