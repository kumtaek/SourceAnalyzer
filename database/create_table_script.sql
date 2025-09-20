------------------------------------------------------------------------------------------------------------------------
-- 프로젝트 메타데이터 (기본 정보만)
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 프로젝트 고유 식별자
    project_name VARCHAR(100) NOT NULL,                -- 프로젝트명 (예: 'sampleSrc', 'ecommerce', 'banking')
    project_path VARCHAR(500) NOT NULL,                -- 프로젝트 상대 경로 (예: 'sampleSrc', './projects/sampleSrc')
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 프로젝트 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 프로젝트 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N'                        -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
);
CREATE UNIQUE INDEX ix_projects_01 ON projects (project_name, project_path);

-- 데이터베이스 테이블 정보
CREATE TABLE IF NOT EXISTS tables (
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 테이블 고유 식별자
    project_id INTEGER NOT NULL,                    -- 프로젝트 ID (projects 테이블 참조)
    component_id INTEGER,                           -- 컴포넌트 ID (components 테이블 참조, TABLE 타입)
    table_name VARCHAR(100) NOT NULL,               -- 테이블명 (예: 'USER_INFO', 'ORDER_MASTER', 'PRODUCT') - 대문자로 변환되서 저장됨.
    table_owner VARCHAR(50) NOT NULL,               -- 테이블 소유자 (예: 'HR', 'SCOTT', 'SYSTEM') - 대문자로 변환되서 저장됨.
    table_comments TEXT,                            -- 테이블 설명/코멘트 (예: '사용자 정보 테이블')
    hash_value VARCHAR(64) NOT NULL,                -- 변경 감지용 해시값 (테이블 구조 기반)
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 테이블 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 테이블 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N',                     -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (component_id) REFERENCES components(component_id)
);
CREATE UNIQUE INDEX ix_tables_01 ON tables (table_name, table_owner, project_id);

-- 데이터베이스 컬럼 정보
CREATE TABLE IF NOT EXISTS columns (
    column_id INTEGER PRIMARY KEY AUTOINCREMENT,       -- 컬럼 고유 식별자
    table_id INTEGER NOT NULL,                        -- 테이블 ID (tables 테이블 참조)
    component_id INTEGER,                              -- 컴포넌트 ID (components 테이블 참조, COLUMN 타입)
    column_name VARCHAR(100) NOT NULL,                 -- 컬럼명 (예: 'USER_ID', 'USER_NAME', 'CREATED_DATE') - 대문자로 변환되서 저장됨.
    data_type VARCHAR(50),                             -- 데이터 타입 (예: 'VARCHAR2', 'NUMBER', 'DATE', 'CLOB')
    data_length INTEGER,                               -- 데이터 길이 (예: VARCHAR2(50)의 50, NUMBER(10,2)의 10)
    nullable CHAR(1) DEFAULT 'Y',                      -- NULL 허용 여부: 'Y'=허용, 'N'=불허용
    column_comments TEXT,                              -- 컬럼 설명/코멘트 (예: '사용자 고유 식별자')
    position_pk INTEGER,                               -- PK 순번 (1,2,3... 또는 NULL=PK 아님)
    data_default TEXT,                                 -- 기본값 (예: 'SYSDATE', '0', 'N')
    owner VARCHAR(50),                                 -- 소유자 (예: 'HR', 'SCOTT', 'SYSTEM') - 대문자로 변환되서 저장됨.
    hash_value VARCHAR(64) NOT NULL,                   -- 변경 감지용 해시값 (컬럼 정의 기반)
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 컬럼 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 컬럼 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N',                        -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
    FOREIGN KEY (table_id) REFERENCES tables(table_id),
    FOREIGN KEY (component_id) REFERENCES components(component_id)
);
CREATE UNIQUE INDEX ix_columns_01 ON columns (table_id, column_name);

------------------------------------------------------------------------------------------------------------------------
-- 파일
CREATE TABLE IF NOT EXISTS files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 파일 고유 식별자
    project_id INTEGER NOT NULL,                   -- 프로젝트 ID (projects 테이블 참조)
    file_path VARCHAR(500) NOT NULL,               -- 파일 디렉토리 경로 (예: 'src/main/java/com/example', 'src/main/webapp')
    file_name VARCHAR(200) NOT NULL,               -- 파일명 (예: 'User.java', 'userList.jsp', 'user-mapper.xml')
    file_type VARCHAR(20) NOT NULL,                -- 파일 타입: 'java', 'jsp', 'xml', 'sql', 'css', 'js', 'html' 등
    hash_value VARCHAR(64) NOT NULL,               -- 변경 감지용 해시값 (파일 내용 기반)
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 파일 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 파일 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N',                    -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
    line_count INTEGER,                            -- 파일 총 라인 수
    file_size INTEGER,                             -- 파일 크기 (바이트)
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
CREATE UNIQUE INDEX ix_files_01 ON files (file_name, file_path, project_id);

-- 1. classes 테이블 생성
CREATE TABLE IF NOT EXISTS classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 클래스 고유 식별자
    project_id INTEGER NOT NULL,                   -- 프로젝트 ID (projects 테이블 참조)
    file_id INTEGER NOT NULL,                      -- 파일 ID (files 테이블 참조)
    class_name VARCHAR(200) NOT NULL,              -- 클래스명 (예: 'UserController', 'UserService', 'User')
    parent_class_id INTEGER,                       -- 상속/구현 부모 클래스 ID (classes 테이블 참조, NULL=최상위 클래스)
    line_start INTEGER,                            -- 클래스 시작 라인 번호
    line_end INTEGER,                              -- 클래스 종료 라인 번호
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 클래스 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 클래스 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N',                    -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);
CREATE UNIQUE INDEX ix_classes_01 ON classes (class_name, file_id, project_id);
CREATE INDEX ix_classes_02 ON classes (parent_class_id);

-- 코드 구성 요소 (클래스, 메서드 등의 기본 정보만)
CREATE TABLE IF NOT EXISTS components (
    component_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 컴포넌트 고유 식별자
    project_id INTEGER NOT NULL,                   -- 프로젝트 ID (projects 테이블 참조)
    file_id INTEGER NOT NULL,                      -- 파일 ID (files 테이블 참조)
    component_name VARCHAR(200) NOT NULL,          -- 컴포넌트명 (예: 'getUserList', 'UserService', 'USER_INFO')
    component_type VARCHAR(20) NOT NULL,           -- 컴포넌트 타입: 'METHOD', 'CLASS', 'SQL_SELECT', 'SQL_INSERT', 'SQL_UPDATE', 'SQL_DELETE', 'QUERY'(INFERRED쿼리), 'TABLE', 'COLUMN', 'API_URL' 등. JSP/JSX/Vue 등 프론트엔드 파일은 files 테이블에만 저장
    parent_id INTEGER,                             -- 부모 컴포넌트 ID: COLUMN일때는 TABLE의 component_id, METHOD일때는 classes의 class_id
    layer VARCHAR(30),                             -- 계층 정보 (예: 'CONTROLLER', 'SERVICE', 'DAO', 'ENTITY')
    line_start INTEGER,                            -- 컴포넌트 시작 라인 번호
    line_end INTEGER,                              -- 컴포넌트 종료 라인 번호
    has_error CHAR(1) DEFAULT 'N',                 -- 오류 여부: 'Y'=오류발생, 'N'=정상
    error_message TEXT,                            -- 오류 발생 시 상세 오류 메시지
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 컴포넌트 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 컴포넌트 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N',                    -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);
CREATE UNIQUE INDEX ix_components_01 ON components (component_name, file_id, project_id);
CREATE INDEX ix_components_parent_id ON components (parent_id);

-- 통합 관계 정보 (모든 관계를 통합 관리)
CREATE TABLE IF NOT EXISTS relationships (
    relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 관계 고유 식별자
    src_id INTEGER NOT NULL,                       -- 소스 컴포넌트 ID (components 테이블 참조)
    dst_id INTEGER NOT NULL,                       -- 대상 컴포넌트 ID (components 테이블 참조)
    rel_type VARCHAR(50) NOT NULL,                -- 관계 타입: 'CALL_METHOD'(API_URL->METHOD, METHOD->METHOD), 'CALL_QUERY'(METHOD->SQL/QUERY), 'USE_TABLE'(SQL/QUERY->TABLE), 'INHERITANCE'(클래스상속), 'JOIN_EXPLICIT'(명시적조인), 'JOIN_IMPLICIT'(암시적조인), 'FK'(외래키) 등
    created_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 관계 등록일시 (한국시간)
    updated_at DATETIME DEFAULT (datetime('now', '+9 hours')),  -- 관계 수정일시 (한국시간)
    del_yn CHAR(1) DEFAULT 'N',                    -- 삭제 여부: 'Y'=삭제됨, 'N'=활성상태
    CHECK (src_id != dst_id)
);
CREATE UNIQUE INDEX ix_relationships_01 ON relationships (src_id, dst_id, rel_type);
 
-- 데이터베이스 최적화 설정
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
PRAGMA temp_store = MEMORY;
PRAGMA foreign_keys = ON;