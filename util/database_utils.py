"""
SourceAnalyzer 데이터베이스 처리 공통 유틸리티 모듈
- SQLite 연결 관리
- 단순한 건건 커밋 구조
- 쿼리 실행 및 스키마 생성
"""

import sqlite3
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from .logger import app_logger, handle_error


class DatabaseUtils:
    """데이터베이스 처리 관련 공통 유틸리티 클래스"""
    
    def __init__(self, db_path: str):
        """
        데이터베이스 유틸리티 초기화
        
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> bool:
        """
        데이터베이스에 연결
        
        Returns:
            연결 성공 여부 (True/False)
        """
        try:
            # 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            
            # 외래키 제약조건 활성화
            self.connection.execute("PRAGMA foreign_keys = ON")
            
            # 성능 최적화 설정
            self.connection.execute("PRAGMA journal_mode = WAL")
            self.connection.execute("PRAGMA synchronous = NORMAL")
            self.connection.execute("PRAGMA cache_size = 10000")
            self.connection.execute("PRAGMA temp_store = MEMORY")
            
            app_logger.debug(f"데이터베이스 연결 성공: {self.db_path}")
            return True
            
        except Exception as e:
            handle_error(e, f"데이터베이스 연결 실패: {self.db_path}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 해제"""
        if self.connection:
            try:
                self.connection.close()
                app_logger.debug(f"데이터베이스 연결 해제: {self.db_path}")
            except Exception as e:
                handle_error(e, f"데이터베이스 연결 해제 실패")
            finally:
                self.connection = None
    
    @contextmanager
    def get_connection(self):
        """
        데이터베이스 연결 컨텍스트 매니저
        
        Yields:
            sqlite3.Connection: 데이터베이스 연결 객체
        """
        conn = None
        try:
            if not self.connection:
                if not self.connect():
                    raise Exception("데이터베이스 연결 실패")
            conn = self.connection
            yield conn
        except Exception as e:
            handle_error(e, f"데이터베이스 연결 오류")
        finally:
            # 연결은 클래스 레벨에서 관리하므로 여기서는 닫지 않음
            pass
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        SELECT 쿼리 실행
        
        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터
            
        Returns:
            쿼리 결과 리스트
        """
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results = []
                for row in cursor.fetchall():
                    results.append(dict(row))
                
                app_logger.debug(f"쿼리 실행 성공: {query[:50]}...")
                return results
                
        except Exception as e:
            handle_error(e, f"쿼리 실행 실패: {query[:50]}...")
    
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        INSERT, UPDATE, DELETE 쿼리 실행 (건건 커밋)
        
        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터
            
        Returns:
            영향받은 행 수
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # 건건 커밋 (단순한 트랜잭션 구조)
                conn.commit()
                affected_rows = cursor.rowcount
                
                app_logger.debug(f"업데이트 쿼리 실행 성공: {query[:50]}..., 영향받은 행: {affected_rows}")
                return affected_rows
                
        except Exception as e:
            handle_error(e, f"업데이트 쿼리 실행 실패: {query[:50]}...")
            return 0
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        여러 개의 파라미터로 쿼리 실행 (배치 처리, 건건 커밋)
        
        Args:
            query: 실행할 SQL 쿼리
            params_list: 파라미터 리스트
            
        Returns:
            처리된 행 수
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 배치 처리
                cursor.executemany(query, params_list)
                
                # 건건 커밋 (단순한 트랜잭션 구조)
                conn.commit()
                
                processed_rows = len(params_list)
                app_logger.debug(f"배치 쿼리 실행 성공: {query[:50]}..., 처리된 행: {processed_rows}")
                return processed_rows
                
        except Exception as e:
            handle_error(e, f"배치 쿼리 실행 실패: {query[:50]}...")
            return 0
    
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        레코드 삽입 (건건 커밋)
        
        Args:
            table_name: 테이블명
            data: 삽입할 데이터 딕셔너리
            
        Returns:
            삽입 성공 여부
        """
        try:
            if not data:
                app_logger.warning(f"삽입할 데이터가 없습니다: {table_name}")
                return False
            
            # 컬럼과 값 분리
            columns = list(data.keys())
            values = list(data.values())
            
            # INSERT 쿼리 생성
            placeholders = ', '.join(['?' for _ in columns])
            columns_str = ', '.join(columns)
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            # 쿼리 실행
            affected_rows = self.execute_update(query, tuple(values))
            
            if affected_rows > 0:
                app_logger.debug(f"레코드 삽입 성공: {table_name}")
                return True
            else:
                app_logger.warning(f"레코드 삽입 실패 (영향받은 행 없음): {table_name}")
                return False
                
        except Exception as e:
            handle_error(e, f"레코드 삽입 실패: {table_name}")
            return False
    
    def update_record(self, table_name: str, update_data: Dict[str, Any], where_conditions: Dict[str, Any]) -> bool:
        """
        레코드 업데이트 (건건 커밋)
        
        Args:
            table_name: 테이블명
            update_data: 업데이트할 데이터 딕셔너리
            where_conditions: WHERE 조건 딕셔너리
            
        Returns:
            업데이트 성공 여부
        """
        try:
            if not update_data:
                app_logger.warning(f"업데이트할 데이터가 없습니다: {table_name}")
                return False
            
            if not where_conditions:
                app_logger.warning(f"WHERE 조건이 없습니다: {table_name}")
                return False
            
            # SET 절 생성
            set_clauses = []
            set_values = []
            for column, value in update_data.items():
                set_clauses.append(f"{column} = ?")
                set_values.append(value)
            
            # WHERE 절 생성
            where_clauses = []
            where_values = []
            for column, value in where_conditions.items():
                where_clauses.append(f"{column} = ?")
                where_values.append(value)
            
            # UPDATE 쿼리 생성
            query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
            
            # 쿼리 실행
            all_values = set_values + where_values
            affected_rows = self.execute_update(query, tuple(all_values))
            
            if affected_rows > 0:
                app_logger.debug(f"레코드 업데이트 성공: {table_name}")
                return True
            else:
                app_logger.warning(f"레코드 업데이트 실패 (영향받은 행 없음): {table_name}")
                return False
                
        except Exception as e:
            handle_error(e, f"레코드 업데이트 실패: {table_name}")
            return False
    
    def delete_record(self, table_name: str, where_conditions: Dict[str, Any]) -> bool:
        """
        레코드 삭제 (건건 커밋)
        
        Args:
            table_name: 테이블명
            where_conditions: WHERE 조건 딕셔너리
            
        Returns:
            삭제 성공 여부
        """
        try:
            if not where_conditions:
                app_logger.warning(f"WHERE 조건이 없습니다: {table_name}")
                return False
            
            # WHERE 절 생성
            where_clauses = []
            where_values = []
            for column, value in where_conditions.items():
                where_clauses.append(f"{column} = ?")
                where_values.append(value)
            
            # DELETE 쿼리 생성
            query = f"DELETE FROM {table_name} WHERE {' AND '.join(where_clauses)}"
            
            # 쿼리 실행
            affected_rows = self.execute_update(query, tuple(where_values))
            
            if affected_rows > 0:
                app_logger.debug(f"레코드 삭제 성공: {table_name}")
                return True
            else:
                app_logger.warning(f"레코드 삭제 실패 (영향받은 행 없음): {table_name}")
                return False
                
        except Exception as e:
            handle_error(e, f"레코드 삭제 실패: {table_name}")
            return False
    
    def create_schema(self, schema_file_path: str) -> bool:
        """
        SQL 스키마 파일로부터 데이터베이스 스키마 생성
        
        Args:
            schema_file_path: 스키마 파일 경로
            
        Returns:
            스키마 생성 성공 여부
        """
        try:
            if not os.path.exists(schema_file_path):
                handle_error(Exception(f"스키마 파일이 존재하지 않습니다: {schema_file_path}"))
                return False
            
            with open(schema_file_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # SQL 스크립트 실행 (세미콜론으로 분리)
            sql_statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for statement in sql_statements:
                    if statement:
                        cursor.execute(statement)
                
                # 건건 커밋
                conn.commit()
            
            app_logger.info(f"데이터베이스 스키마 생성 완료: {schema_file_path}")
            return True
            
        except Exception as e:
            handle_error(e, f"데이터베이스 스키마 생성 실패: {schema_file_path}")
            return False
    
    def table_exists(self, table_name: str) -> bool:
        """
        테이블 존재 여부 확인
        
        Args:
            table_name: 확인할 테이블명
            
        Returns:
            테이블 존재 여부
        """
        try:
            query = """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """
            results = self.execute_query(query, (table_name,))
            return len(results) > 0
            
        except Exception as e:
            handle_error(e, f"테이블 존재 여부 확인 실패: {table_name}")
            return False
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        테이블 구조 정보 조회
        
        Args:
            table_name: 테이블명
            
        Returns:
            테이블 구조 정보 리스트
        """
        try:
            query = f"PRAGMA table_info({table_name})"
            return self.execute_query(query)
            
        except Exception as e:
            handle_error(e, f"테이블 구조 정보 조회 실패: {table_name}")
            return []


# 편의 함수들
def create_database_connection(db_path: str) -> DatabaseUtils:
    """
    데이터베이스 연결 생성 편의 함수
    
    Args:
        db_path: 데이터베이스 파일 경로
        
    Returns:
        DatabaseUtils 인스턴스
    """
    db_utils = DatabaseUtils(db_path)
    if db_utils.connect():
        return db_utils
    else:
        handle_error(Exception(f"데이터베이스 연결 실패: {db_path}"))
        return None


def execute_sql_script(db_utils: DatabaseUtils, script_path: str) -> bool:
    """
    SQL 스크립트 실행 편의 함수
    
    Args:
        db_utils: DatabaseUtils 인스턴스
        script_path: SQL 스크립트 파일 경로
        
    Returns:
        실행 성공 여부
    """
    return db_utils.create_schema(script_path)
