#!/usr/bin/env python3
"""
SourceAnalyzer 메인 실행기
연관관계 도출 중심의 소스코드 분석 파이프라인

사용법:
    python main.py --project-name SampleSrc --clear-metadb
    python main.py --project-name SampleSrc  # 드라이런
"""

import sys
import argparse
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from util.logger import get_logger, handle_error
from util.arg_utils import parse_arguments
from core.pipeline import SourceAnalyzerPipeline

logger = get_logger(__name__)

def main():
    """메인 실행 함수"""
    try:
        # 1. 명령행 인수 파싱
        args = parse_arguments()
        logger.info(f"SourceAnalyzer 시작 - 프로젝트: {args.project_name}")
        
        # 2. 파이프라인 초기화
        pipeline = SourceAnalyzerPipeline(
            project_name=args.project_name,
            clear_metadb=args.clear_metadb,
            dry_run=args.dry_run
        )
        
        # 3. 파이프라인 실행
        pipeline.run()
        
        logger.info("SourceAnalyzer 완료")
        
    except Exception as e:
        handle_error(f"메인 실행 실패: {str(e)}", e)

if __name__ == "__main__":
    main()
