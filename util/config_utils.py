"""
SourceAnalyzer 설정 파일 처리 공통 유틸리티 모듈
- YAML 설정 파일 로드
- 설정 값 조회 및 검증
- 프로젝트별 설정 관리
"""

import os
import yaml
from typing import Any, Dict, Optional, Union
from .logger import app_logger, handle_error
from .path_utils import PathUtils


class ConfigUtils:
    """설정 파일 처리 관련 공통 유틸리티 클래스"""
    
    def __init__(self):
        """ConfigUtils 초기화"""
        self.path_utils = PathUtils()
        self._config_cache = {}
    
    def load_yaml_config(self, config_path: str) -> Dict[str, Any]:
        """
        YAML 설정 파일 로드
        
        Args:
            config_path: 설정 파일 경로
            
        Returns:
            설정 딕셔너리
        """
        try:
            # 절대 경로로 변환
            abs_config_path = self.path_utils.normalize_path(config_path)
            
            if not self.path_utils.exists(abs_config_path):
                handle_error(Exception(f"설정 파일이 존재하지 않습니다: {abs_config_path}"))
            
            # 캐시 확인
            if abs_config_path in self._config_cache:
                app_logger.debug(f"설정 파일 캐시에서 로드: {abs_config_path}")
                return self._config_cache[abs_config_path]
            
            # YAML 파일 로드
            with open(abs_config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config is None:
                config = {}
            
            # 캐시에 저장
            self._config_cache[abs_config_path] = config
            
            app_logger.debug(f"설정 파일 로드 성공: {abs_config_path}")
            return config
            
        except Exception as e:
            handle_error(e, f"설정 파일 로드 실패: {config_path}")
            return {}
    
    def get_config_value(self, config: Dict[str, Any], key_path: str, default_value: Any = None) -> Any:
        """
        설정 값 조회 (점 표기법 지원)
        
        Args:
            config: 설정 딕셔너리
            key_path: 키 경로 (예: 'database.host', 'parser.java.enabled')
            default_value: 기본값
            
        Returns:
            설정 값 또는 기본값
        """
        try:
            keys = key_path.split('.')
            current_value = config
            
            for key in keys:
                if isinstance(current_value, dict) and key in current_value:
                    current_value = current_value[key]
                else:
                    app_logger.debug(f"설정 키를 찾을 수 없음: {key_path}, 기본값 사용: {default_value}")
                    return default_value
            
            app_logger.debug(f"설정 값 조회 성공: {key_path} = {current_value}")
            return current_value
            
        except Exception as e:
            handle_error(e, f"설정 값 조회 실패: {key_path}")
            return default_value
    
    def validate_config(self, config: Dict[str, Any], required_keys: list) -> bool:
        """
        설정 유효성 검사
        
        Args:
            config: 설정 딕셔너리
            required_keys: 필수 키 목록
            
        Returns:
            유효성 검사 통과 여부
        """
        try:
            missing_keys = []
            
            for key in required_keys:
                if self.get_config_value(config, key) is None:
                    missing_keys.append(key)
            
            if missing_keys:
                app_logger.error(f"필수 설정 키 누락: {missing_keys}")
                return False
            
            app_logger.debug(f"설정 유효성 검사 통과")
            return True
            
        except Exception as e:
            handle_error(e, f"설정 유효성 검사 실패")
            return False
    
    def load_project_config(self, project_name: str) -> Dict[str, Any]:
        """
        프로젝트별 설정 로드
        
        Args:
            project_name: 프로젝트명
            
        Returns:
            프로젝트 설정 딕셔너리
        """
        try:
            config_path = self.path_utils.join_path("projects", project_name, "config", "target_source_config.yaml")
            return self.load_yaml_config(config_path)
            
        except Exception as e:
            handle_error(e, f"프로젝트 설정 로드 실패: {project_name}")
            return {}
    
    def get_main_config(self) -> Dict[str, Any]:
        """
        메인 설정 파일 로드
        
        Returns:
            메인 설정 딕셔너리
        """
        try:
            config_path = self.path_utils.join_path("config", "config.yaml")
            return self.load_yaml_config(config_path)
            
        except Exception as e:
            handle_error(e, f"메인 설정 로드 실패")
            return {}
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        로깅 설정 파일 로드
        
        Returns:
            로깅 설정 딕셔너리
        """
        try:
            config_path = self.path_utils.join_path("config", "logging.yaml")
            return self.load_yaml_config(config_path)
            
        except Exception as e:
            handle_error(e, f"로깅 설정 로드 실패")
            return {}
    
    def get_parser_config(self, parser_name: str) -> Dict[str, Any]:
        """
        파서별 설정 파일 로드
        
        Args:
            parser_name: 파서명 (예: 'java', 'xml', 'vue')
            
        Returns:
            파서 설정 딕셔너리
        """
        try:
            config_path = self.path_utils.join_path("config", "parser", f"{parser_name}_rules.yaml")
            return self.load_yaml_config(config_path)
            
        except Exception as e:
            app_logger.warning(f"파서 설정 파일이 없습니다: {parser_name}")
            return {}
    
    def clear_cache(self):
        """설정 캐시 초기화"""
        self._config_cache.clear()
        app_logger.debug("설정 캐시 초기화 완료")
    
    def reload_config(self, config_path: str) -> Dict[str, Any]:
        """
        설정 파일 재로드 (캐시 무시)
        
        Args:
            config_path: 설정 파일 경로
            
        Returns:
            설정 딕셔너리
        """
        try:
            abs_config_path = self.path_utils.normalize_path(config_path)
            
            # 캐시에서 제거
            if abs_config_path in self._config_cache:
                del self._config_cache[abs_config_path]
            
            # 재로드
            return self.load_yaml_config(config_path)
            
        except Exception as e:
            handle_error(e, f"설정 파일 재로드 실패: {config_path}")
            return {}


# 편의 함수들
def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """YAML 설정 파일 로드 편의 함수"""
    config_utils = ConfigUtils()
    return config_utils.load_yaml_config(config_path)


def get_config_value(config: Dict[str, Any], key_path: str, default_value: Any = None) -> Any:
    """설정 값 조회 편의 함수"""
    config_utils = ConfigUtils()
    return config_utils.get_config_value(config, key_path, default_value)
