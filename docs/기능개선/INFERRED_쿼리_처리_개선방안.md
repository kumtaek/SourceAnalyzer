# INFERRED 쿼리 처리 개선 방안

## 문서 정보
- **작성일**: 2025-09-19
- **버전**: v1.0
- **목적**: INFERRED 쿼리 처리 로직 개선 및 중복 방지

## 1. 문제점 분석

### 1.1 발견된 문제점
- Java 파서가 `component_type = 'QUERY'`로만 검색하여 XML에서 생성된 `SQL_*` 타입을 찾지 못함
- 결과적으로 모든 쿼리를 inferred query로 중복 생성하여 데이터 중복 발생

### 1.2 현재 처리 방식의 한계
```python
# 현재: XML에서 생성된 SQL_* 타입을 찾지 못함
existing_queries = cursor.execute("""
    SELECT component_id, component_name 
    FROM components 
    WHERE project_id = ? AND component_type = 'QUERY'
""", [project_id]).fetchall()
```

**문제점**:
- XML에서 생성된 `SQL_SELECT`, `SQL_INSERT`, `SQL_UPDATE`, `SQL_DELETE` 타입은 검색되지 않음
- Java에서 호출하는 쿼리가 이미 XML에 정의되어 있어도 중복 생성됨

## 2. 해결 방안

### 2.1 쿼리 검색 로직 개선

#### 개선된 검색 쿼리
```python
# 개선: SQL_* 타입과 QUERY 타입 모두 검색
existing_queries = cursor.execute("""
    SELECT component_id, component_name, component_type
    FROM components 
    WHERE project_id = ? 
      AND (component_type LIKE 'SQL_%' OR component_type = 'QUERY')
      AND del_yn = 'N'
""", [project_id]).fetchall()
```

#### 매칭 로직 개선
```python
def find_existing_query(query_name: str, existing_queries: List[dict]) -> Optional[dict]:
    """기존 쿼리 검색 (SQL_* 타입 포함)"""
    
    # 1. 정확한 이름 매칭
    for query in existing_queries:
        if query['component_name'] == query_name:
            return query
    
    # 2. 유사 이름 매칭 (네임스페이스 제거)
    clean_query_name = query_name.split('.')[-1]  # com.example.getUserById -> getUserById
    
    for query in existing_queries:
        clean_existing_name = query['component_name'].split('.')[-1]
        if clean_existing_name == clean_query_name:
            return query
    
    return None
```

### 2.2 INFERRED 쿼리 정보 보강

#### 자바 호출 위치 정보 저장
```python
def create_inferred_query(query_name: str, java_file_info: dict) -> dict:
    """INFERRED 쿼리 생성 (자바 호출 정보 포함)"""
    
    return {
        'component_name': query_name,
        'component_type': 'QUERY',  # 정확한 SQL 타입을 알 수 없음
        'file_id': java_file_info['file_id'],  # Java 파일 ID
        'line_start': java_file_info['line_start'],  # 호출 위치
        'line_end': java_file_info['line_end'],
        'layer': 'QUERY',
        'has_error': 'N',
        'error_message': f'INFERRED from Java: {java_file_info["file_name"]}'
    }
```

### 2.3 테이블 관계 연결 개선

#### SQL_* 타입과 QUERY 타입 모두 처리
```python
def create_table_relationships(query_component_id: int, table_names: List[str]):
    """테이블 관계 생성 (모든 쿼리 타입 지원)"""
    
    relationships = []
    
    for table_name in table_names:
        # 테이블 검색 (실제 스키마 우선)
        table_component = find_table_component(table_name)
        
        if table_component:
            relationships.append({
                'src_id': query_component_id,
                'dst_id': table_component['component_id'],
                'rel_type': 'USE_TABLE'
            })
    
    return relationships
```

## 3. components 테이블 활용 개선

### 3.1 쿼리 컴포넌트 타입 (v4.0 개선)
- `SQL_SELECT`: **XML/Java 모두에서** 파싱된 SELECT 쿼리
- `SQL_INSERT`: **XML/Java 모두에서** 파싱된 INSERT 쿼리  
- `SQL_UPDATE`: **XML/Java 모두에서** 파싱된 UPDATE 쿼리
- `SQL_DELETE`: **XML/Java 모두에서** 파싱된 DELETE 쿼리
- `QUERY`: Java에서 추론된 INFERRED 쿼리 (정확한 SQL 타입을 모름)

### 3.2 INFERRED 쿼리 특징
- `component_type = 'QUERY'` (정확한 SQL 타입을 알 수 없기 때문)
- `line_start`, `line_end`: 자바에서 쿼리를 호출하는 실제 라인 번호
- `file_id`: 자바 파일의 file_id (XML 파일이 아닌 실제 호출 파일)

## 4. sql_contents 테이블 활용

### 4.1 Java SQL 처리 기능 (v4.0 신규)

#### Java에서 지원하는 SQL 패턴
- ✅ **StringBuilder 패턴**: `StringBuilder query = new StringBuilder(); query.append("SELECT ...")`
- ❌ **+ 연산자 패턴**: `String query = "SELECT " + "FROM users"` (미지원)
- ❌ **String.format 패턴**: `String.format("SELECT * FROM %s", tableName)` (미지원)

#### Java SQL 컴포넌트 타입
- ✅ **SQL_SELECT**: SELECT 쿼리 (StringBuilder에서 추출)
- ✅ **SQL_INSERT**: INSERT 쿼리 (StringBuilder에서 추출)  
- ✅ **SQL_UPDATE**: UPDATE 쿼리 (StringBuilder에서 추출)
- ✅ **SQL_DELETE**: DELETE 쿼리 (StringBuilder에서 추출)
- ❌ **SQL_MERGE**: MERGE 쿼리 (아직 미지원)

#### 압축 저장 처리
- `SqlContentProcessor`를 통한 gzip 압축 저장
- `SqlContent.db`에 별도 관리
- XML과 Java 모두 동일한 방식으로 처리

### 4.2 sql_contents 테이블 활용

#### XML/Java 공통 SQL 내용 저장
- `component_id`: SQL 컴포넌트의 component_id
- `sql_content_compressed`: gzip 압축된 SQL 내용 (XML 파싱 결과 또는 Java StringBuilder 추출 결과)
- `query_type`: 정확한 SQL 타입 (SQL_SELECT, SQL_INSERT, SQL_UPDATE, SQL_DELETE)
- `file_path`: 원본 파일 경로 (XML 또는 Java)
- `line_start/line_end`: 실제 라인 번호 (Java의 경우 StringBuilder 위치)

## 5. relationships 테이블 활용

### 5.1 CALL_QUERY 관계
- `src_id`: Java METHOD의 component_id
- `dst_id`: SQL 쿼리의 component_id (SQL_* 또는 QUERY 타입)
- `rel_type = 'CALL_QUERY'`

### 5.2 USE_TABLE 관계
- `src_id`: SQL 쿼리의 component_id (SQL_* 또는 QUERY 타입 모두 처리)
- `dst_id`: TABLE의 component_id
- `rel_type = 'USE_TABLE'`

## 6. 구현 예시

### 6.1 개선된 Java 파서 로직
```python
class ImprovedJavaParser:
    """개선된 Java 파서"""
    
    def process_sql_calls(self, project_id: int, java_file_info: dict):
        """SQL 호출 처리 (중복 방지)"""
        
        # 1. 기존 쿼리 조회 (SQL_* 타입 포함)
        existing_queries = self.get_existing_queries(project_id)
        
        # 2. Java에서 SQL 호출 추출
        sql_calls = self.extract_sql_calls(java_file_info['content'])
        
        for sql_call in sql_calls:
            # 3. 기존 쿼리 검색
            existing_query = self.find_existing_query(sql_call['name'], existing_queries)
            
            if existing_query:
                # 4-1. 기존 쿼리 사용
                query_component_id = existing_query['component_id']
                print(f"Using existing query: {sql_call['name']} (type: {existing_query['component_type']})")
            else:
                # 4-2. INFERRED 쿼리 생성
                query_component_id = self.create_inferred_query(sql_call, java_file_info)
                print(f"Created INFERRED query: {sql_call['name']}")
            
            # 5. 메서드 -> 쿼리 관계 생성
            self.create_method_query_relationship(sql_call['method_id'], query_component_id)
    
    def get_existing_queries(self, project_id: int) -> List[dict]:
        """기존 쿼리 조회 (개선된 버전)"""
        
        return self.db.execute("""
            SELECT component_id, component_name, component_type, file_id
            FROM components 
            WHERE project_id = ? 
              AND (component_type LIKE 'SQL_%' OR component_type = 'QUERY')
              AND del_yn = 'N'
            ORDER BY 
              CASE WHEN component_type LIKE 'SQL_%' THEN 1 ELSE 2 END,  -- SQL_* 타입 우선
              component_id
        """, [project_id]).fetchall()
```

### 6.2 쿼리 매칭 로직
```python
def find_existing_query(self, query_name: str, existing_queries: List[dict]) -> Optional[dict]:
    """기존 쿼리 검색 (개선된 매칭)"""
    
    # 1. 정확한 이름 매칭 (SQL_* 타입 우선)
    for query in existing_queries:
        if query['component_name'] == query_name:
            return query
    
    # 2. 네임스페이스 제거 후 매칭
    clean_name = query_name.split('.')[-1] if '.' in query_name else query_name
    
    for query in existing_queries:
        existing_clean_name = query['component_name'].split('.')[-1] if '.' in query['component_name'] else query['component_name']
        if existing_clean_name == clean_name:
            return query
    
    # 3. 유사 패턴 매칭 (선택적)
    for query in existing_queries:
        if self.is_similar_query_name(query_name, query['component_name']):
            return query
    
    return None

def is_similar_query_name(self, name1: str, name2: str) -> bool:
    """쿼리 이름 유사성 검사"""
    
    # 간단한 유사성 검사 (필요에 따라 확장)
    name1_lower = name1.lower().replace('_', '').replace('-', '')
    name2_lower = name2.lower().replace('_', '').replace('-', '')
    
    return name1_lower == name2_lower
```

## 7. 개선 효과

### 7.1 중복 방지
- XML에서 생성된 `SQL_*` 타입을 정상적으로 활용
- 동일한 쿼리에 대한 중복 생성 방지
- 메타데이터베이스 크기 최적화

### 7.2 정확한 추적
- 끊어진 쿼리의 정확한 자바 호출 위치 파악
- XML 정의 누락 쿼리 식별 가능
- 호출 체인의 완전성 확보

### 7.3 개발 효율성
- 누락된 XML 쿼리 정의를 쉽게 찾아 수정 가능
- INFERRED 쿼리를 통한 미완성 매핑 식별
- 개발 과정에서의 품질 관리 향상

### 7.4 문서화 자동화
- 자동으로 쿼리 호출 관계 문서화
- 영향평가 시 정확한 관계 정보 제공
- 시스템 이해도 향상

## 8. 구현 우선순위

### Phase 1: 기본 개선
1. 쿼리 검색 로직 개선 (SQL_* 타입 포함)
2. 중복 생성 방지 로직 구현
3. 기존 코드 테스트 및 검증

### Phase 2: 고도화
1. 유사 이름 매칭 로직 구현
2. SQL 내용 비교를 통한 정확도 향상
3. 성능 최적화

### Phase 3: 확장
1. 새로운 SQL 패턴 지원 확대
2. 자동 XML 매핑 제안 기능
3. 품질 지표 및 리포트 개선

---

**작성자**: SourceAnalyzer Team  
**작성일**: 2025-09-19  
**관련 문서**: [02_데이터베이스_스키마_정의서.md](../02_데이터베이스_스키마_정의서.md)

