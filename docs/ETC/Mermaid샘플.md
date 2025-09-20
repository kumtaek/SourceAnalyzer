# Mermaid 다이어그램 샘플 모음 (MarkText/Zettlr 호환)

이 문서는 MarkText, Zettlr 등 구버전 Mermaid 환경에서 안전하게 사용할 수 있는 다이어그램 샘플을 제공합니다.

## 1. 플로우차트 (Flowchart)
프로세스나 워크플로우를 시각화하는 기본적인 차트입니다.

```mermaid
flowchart TD
    A["시작"] --> B{"조건 확인"}
    B -->|Yes| C["처리 실행"]
    B -->|No| D["대안 처리"]
    C --> E["결과 저장"]
    D --> E
    E --> F["완료"]
    
    style A fill:#e1f5fe
    style F fill:#c8e6c9
    style B fill:#fff3e0
```

## 2. 시퀀스 다이어그램 (Sequence Diagram)
객체 간의 상호작용과 메시지 흐름을 시간순으로 보여줍니다.

```mermaid
sequenceDiagram
    participant U as 사용자
    participant WS as 웹서버
    participant DB as 데이터베이스
    
    U->>WS: 로그인 요청
    WS->>DB: 사용자 정보 조회
    DB-->>WS: 사용자 데이터 반환
    WS-->>U: 로그인 성공 응답
    
    Note over U,DB: 인증 완료
```

## 3. 클래스 다이어그램 (Class Diagram)
객체지향 프로그래밍에서 클래스 간의 관계를 표현합니다.

```mermaid
classDiagram
    class User {
        +name
        +email
        +age
        +login()
        +logout()
        +updateProfile()
    }
    
    class Order {
        +orderId
        +orderDate
        +totalAmount
        +createOrder()
        +cancelOrder()
    }
    
    class Product {
        +productId
        +productName
        +price
        +updatePrice()
    }
    
    User --> Order : places
    Order --> Product : contains
```

## 4. 상태 다이어그램 (State Diagram)
시스템이나 객체의 상태 변화를 나타냅니다.

```mermaid
stateDiagram-v2
    [*] --> 대기중
    대기중 --> 처리중 : 요청받음
    처리중 --> 완료 : 처리성공
    처리중 --> 오류 : 처리실패
    오류 --> 대기중 : 재시도
    완료 --> [*]
    
    처리중 : 진행률 표시
    오류 : 에러 메시지 출력
```

## 5. 간트 차트 (Gantt Chart)
프로젝트 일정과 작업 진행 상황을 시각화합니다.

```mermaid
gantt
    title 프로젝트 일정 관리
    dateFormat YYYY-MM-DD
    section 기획단계
    요구사항분석      :done, req, 2024-01-01, 2024-01-07
    설계문서작성     :done, design, 2024-01-05, 2024-01-12
    section 개발단계
    프론트엔드개발    :active, frontend, 2024-01-10, 2024-01-25
    백엔드개발       :backend, 2024-01-15, 2024-01-30
    section 테스트단계
    단위테스트       :test1, 2024-01-25, 2024-02-05
    통합테스트       :test2, 2024-02-01, 2024-02-10
```

## 6. 파이 차트 (Pie Chart)
데이터의 비율을 원형 차트로 표현합니다.

```mermaid
pie title 프로그래밍 언어 사용 비율
    "JavaScript" : 35
    "Python" : 25
    "Java" : 20
    "C++" : 12
    "기타" : 8
```

## 7. 깃 브랜치 구조 (Git Graph → Graph로 구현)
Git 저장소의 브랜치와 커밋 히스토리를 시각화합니다.

```mermaid
graph TD
    subgraph "Main Branch"
        M1["초기 설정"]
        M2["기능 통합"]
        M3["v1.0 릴리즈"]
    end
    
    subgraph "Develop Branch"
        D1["기본 기능 구현"]
        D2["테스트 추가"]
        D3["병합 준비"]
    end
    
    subgraph "Feature Branch"
        F1["새 기능 개발"]
        F2["버그 수정"]
    end
    
    M1 --> D1
    D1 --> D2
    D2 --> F1
    F1 --> F2
    F2 --> D3
    D3 --> M2
    M2 --> M3
    
    style M1 fill:#e8f5e8
    style M2 fill:#e8f5e8
    style M3 fill:#e8f5e8
    style D1 fill:#fff3e0
    style D2 fill:#fff3e0
    style D3 fill:#fff3e0
    style F1 fill:#e3f2fd
    style F2 fill:#e3f2fd
```

## 8. ER 다이어그램 (Entity Relationship Diagram)
데이터베이스의 엔티티와 관계를 모델링합니다.

```mermaid
erDiagram
    CUSTOMER {
        int customer_id PK
        string customer_name
        string email
        string phone
    }
    
    ORDER {
        int order_id PK
        int customer_id FK
        date order_date
        decimal total_amount
    }
    
    PRODUCT {
        int product_id PK
        string product_name
        decimal price
        int stock_quantity
    }
    
    ORDER_ITEM {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
    
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : includes
```

## 9. 사용자 여정 (User Journey)
사용자의 경험과 감정 변화를 단계별로 표현합니다.

```mermaid
journey
    title 온라인 쇼핑 사용자 여정
    section 상품 검색
      웹사이트 방문        : 3: 사용자
      상품 검색           : 4: 사용자
      상품 상세 확인       : 5: 사용자
    section 구매 결정
      가격 비교           : 3: 사용자
      리뷰 확인           : 4: 사용자
      장바구니 담기        : 5: 사용자
    section 결제 과정
      회원가입/로그인      : 2: 사용자
      배송 정보 입력       : 3: 사용자
      결제 진행           : 4: 사용자
    section 주문 완료
      주문 확인 메일       : 5: 사용자
      배송 추적           : 4: 사용자
      상품 수령           : 5: 사용자
```

---

## 미지원 다이어그램의 대체 방법

### 10. 개념 구조도 (Mindmap → Graph로 구현)
아이디어나 개념을 중심에서 가지치기 형태로 정리합니다.

```mermaid
graph TD
    ROOT["웹 개발"]
    
    subgraph "프론트엔드"
        HTML["HTML"]
        CSS["CSS"]
        JS["JavaScript"]
        
        HTML --> TAG["시맨틱 태그"]
        HTML --> ACC["접근성"]
        CSS --> RES["반응형 디자인"]
        CSS --> ANI["애니메이션"]
        JS --> ES6["ES6+"]
        JS --> FW["프레임워크"]
        FW --> REACT["React"]
        FW --> VUE["Vue"]
        FW --> ANG["Angular"]
    end
    
    subgraph "백엔드"
        SERVER["서버"]
        DATABASE["데이터베이스"]
        API["API"]
        
        SERVER --> NODE["Node.js"]
        SERVER --> PY["Python"]
        SERVER --> JAVA["Java"]
        DATABASE --> MYSQL["MySQL"]
        DATABASE --> MONGO["MongoDB"]
        DATABASE --> PG["PostgreSQL"]
        API --> REST["REST"]
        API --> GQL["GraphQL"]
    end
    
    subgraph "도구"
        VCS["버전 관리"]
        BUILD["빌드 도구"]
        TEST["테스트"]
        
        VCS --> GIT["Git"]
        VCS --> GITHUB["GitHub"]
        BUILD --> WP["Webpack"]
        BUILD --> VITE["Vite"]
        TEST --> JEST["Jest"]
        TEST --> CY["Cypress"]
    end
    
    ROOT --> HTML
    ROOT --> SERVER
    ROOT --> VCS
    
    style ROOT fill:#e8f5e8
    style HTML fill:#e3f2fd
    style SERVER fill:#fff3e0
    style VCS fill:#ffcc80
```

### 11. 타임라인 (Timeline → Gantt Chart로 구현)
시간순으로 이벤트나 마일스톤을 표시합니다.

```mermaid
gantt
    title 회사 발전 역사 타임라인
    dateFormat YYYY-MM-DD
    axisFormat %Y-%m
    
    section 창업기
    회사설립               :milestone, m1, 2020-01-15, 0d
    첫직원채용            :milestone, m2, 2020-02-01, 0d
    첫제품출시            :milestone, m3, 2020-06-15, 0d
    시드투자유치          :milestone, m4, 2020-07-01, 0d
    
    section 성장기
    사용자1만명돌파       :milestone, m5, 2021-03-15, 0d
    팀확장10명           :milestone, m6, 2021-04-01, 0d
    시리즈A투자          :milestone, m7, 2021-12-15, 0d
    해외진출              :milestone, m8, 2022-01-01, 0d
    
    section 확장기
    사용자10만명돌파      :milestone, m9, 2022-06-15, 0d
    새오피스이전          :milestone, m10, 2022-07-01, 0d
    시리즈B투자          :milestone, m11, 2023-01-15, 0d
    글로벌서비스런칭      :milestone, m12, 2023-02-01, 0d
```

#### 기간이 있는 작업 버전 (실제 작업 기간 표현)

```mermaid
gantt
    title 실제 개발 작업 일정
    dateFormat YYYY-MM-DD
    axisFormat %m월
    
    section 기획단계
    요구사항분석      :done, req, 2024-01-01, 7d
    설계문서작성     :done, design, 2024-01-08, 10d
    
    section 개발단계
    프론트엔드개발    :active, frontend, 2024-01-18, 15d
    백엔드개발       :backend, 2024-01-25, 20d
    APIXMLJava통합   :integration, 2024-02-10, 8d
    
    section 테스트단계
    단위테스트       :test1, 2024-02-18, 10d
    통합테스트       :test2, 2024-02-25, 12d
    성능테스트       :test3, 2024-03-05, 5d
```

### 12. 우선순위 매트릭스 (QuadrantChart → Graph로 구현)
두 축을 기준으로 항목들을 4개 영역으로 분류합니다.

```mermaid
graph TD
    subgraph "높은 우선순위"
        A["버그 수정<br/>긴급+중요"]
        B["성능 최적화<br/>중요함"]
    end
    
    subgraph "중간 우선순위"
        C["코드 리뷰<br/>정기적 수행"]
        D["새 기능 개발<br/>계획된 작업"]
    end
    
    subgraph "낮은 우선순위"
        E["문서 작성<br/>여유시 진행"]
        F["이메일 확인<br/>일상 업무"]
        G["회의 참석<br/>필요시만"]
    end
    
    A --> C
    B --> D
    C --> E
    D --> F
    
    style A fill:#ff6b6b
    style B fill:#ffa726
    style C fill:#66bb6a
    style D fill:#66bb6a
    style E fill:#90a4ae
    style F fill:#90a4ae
    style G fill:#90a4ae
```

### 13. 요구사항 관계도 (RequirementDiagram → Graph로 구현)
시스템 요구사항과 그 관계를 표현합니다.

```mermaid
graph TD
    subgraph "핵심 요구사항 (고위험)"
        REQ001["REQ001: 사용자 인증<br/>안전한 로그인 필수<br/>검증방법: 테스트"]
        REQ002["REQ002: 데이터 보안<br/>개인정보 암호화<br/>검증방법: 검사"]
    end
    
    subgraph "성능 요구사항 (중위험)"
        REQ003["REQ003: 응답 속도<br/>3초 이내 로딩<br/>검증방법: 실증"]
    end
    
    subgraph "사용성 요구사항 (저위험)"
        REQ004["REQ004: 사용성<br/>직관적 인터페이스<br/>검증방법: 분석"]
    end
    
    subgraph "시스템 컴포넌트"
        SYS1["인증 시스템"]
        SYS2["데이터베이스"]
        SYS3["웹 서버"]
        SYS4["UI 컴포넌트"]
    end
    
    SYS1 --> REQ001
    SYS2 --> REQ002
    SYS3 --> REQ003
    SYS4 --> REQ004
    
    REQ001 -.-> REQ002
    REQ003 -.-> REQ004
    
    style REQ001 fill:#ffcdd2
    style REQ002 fill:#ffcdd2
    style REQ003 fill:#fff3e0
    style REQ004 fill:#e8f5e8
    style SYS1 fill:#e3f2fd
    style SYS2 fill:#e3f2fd
    style SYS3 fill:#e3f2fd
    style SYS4 fill:#e3f2fd
```

---

## 참고사항

### Mermaid 에러 방지 팁
1. **HTML 태그**: `<tag>` → `&lt;tag&gt;`로 변환
2. **줄바꿈**: `\n` 우선, 안되면 `<br/>` 사용
3. **긴 라벨**: `"내용"` 큰따옴표로 감싸기
4. **이모지**: 단순 기호 사용 (`✔`, `✗`)
5. **중복 정의**: 같은 관계나 스타일 중복 제거
6. **시퀀스 다이어그램**: participant 식별자는 영문, `as` 키워드로 한글 표시
7. **초기화 블록**: 큰따옴표 JSON (`{"theme":"default"}`)
8. **화살표**: `->` 사용 (유니코드 `→` 금지)
9. **간트차트**: 한글에서 공백/특수문자 제거 (파일 스캔 → 파일스캔, XML/Java → XMLJava)
10. **클래스다이어그램**: 타입 제거 (+String name → +name), 단순 관계 (||--o{ → -->)

### MarkText/Zettlr 완전 지원 다이어그램 (최종 확정)
- ✅ `flowchart` / `graph`: 플로우차트, 네트워크, 마인드맵, 요구사항, Git브랜치
- ✅ `sequenceDiagram`: 시퀀스 다이어그램 (participant는 영문 필수)
- ✅ `classDiagram`: 클래스 다이어그램 (타입 제거, 단순 관계)
- ✅ `stateDiagram-v2`: 상태 다이어그램
- ✅ `gantt`: 간트 차트 (공백/특수문자 제거, 타임라인 표현 가능)
- ✅ `pie`: 파이 차트
- ✅ `erDiagram`: ER 다이어그램

### 구버전 미지원 → 대체 방법 (필수 적용)
- ❌ `timeline` (v9+) → ✅ `gantt`의 `milestone` 사용
- ❌ `quadrantChart` (v9+) → ✅ `graph`의 `subgraph` 사용
- ❌ `requirementDiagram` (v9+) → ✅ `graph`의 `subgraph`로 요구사항 표현
- ❌ `mindmap` (v9+) → ✅ `graph`의 계층 구조로 개념 표현
- ❌ `gitgraph` (미지원) → ✅ `graph`의 `subgraph`로 브랜치 구조 표현
- ❌ `journey` (일부 환경 불안정) → ✅ `flowchart`로 단계별 흐름 표현

### 완전 호환 보장
✅ 위 대체 방법을 사용하면 MarkText/Zettlr에서 100% 호환됩니다.

### 환경별 대응 가이드

#### MarkText 사용 시
- `\n` 대신 `<br/>` 태그 우선 사용
- 복잡한 한글 라벨은 반드시 큰따옴표로 감싸기
- 특수문자 포함 시 HTML 엔티티 사용

#### VS Code + Mermaid Extension
- 표준 `\n` 문법 정상 동작
- 실시간 미리보기에서 오류 확인 가능

#### GitHub/GitLab
- 표준 Mermaid 문법 지원
- 이모지 지원 제한적

### 디버깅 방법

#### 1. 단계별 축소
복잡한 다이어그램에서 오류 발생 시:
1. 노드 하나씩 제거하면서 테스트
2. 오류 발생 지점 특정
3. 해당 부분만 수정

#### 2. 브라우저 개발자 도구 활용
- F12 → Console 탭에서 Mermaid 오류 메시지 확인
- 구체적인 파싱 오류 위치 파악 가능

#### 3. 온라인 Mermaid 에디터 활용
- https://mermaid.live/ 에서 테스트
- 실시간으로 오류 확인 및 수정

### 최종 요약

#### ✅ 안전한 작성법
1. HTML 태그: `&lt;tag&gt;` 사용
2. 줄바꿈: `\n` 우선, 안되면 `<br/>` 사용  
3. 긴 라벨: `"내용"` 큰따옴표로 감싸기
4. 이모지: 단순 기호 사용 (`✔`, `✗`)
5. 중복: 관계/스타일 중복 제거
6. ERD: 단순 문법만 사용 (PK/FK 불가)
7. init: 큰따옴표 JSON (`{"theme":"default"}`)
8. 화살표: `->` 사용 (유니코드 `→` 금지)
9. 시퀀스: participant 식별자는 영문, `as`로 한글 표시

#### 🔧 문제 해결 순서
1. **기본 문법 확인**: 표준 Mermaid 문법 준수
2. **환경 확인**: 사용 중인 뷰어/에디터 특성 파악
3. **단계적 수정**: 복잡한 부분부터 단순화
4. **테스트**: 온라인 에디터에서 검증
5. **적용**: 실제 환경에 반영

**작성일**: 2025-09-19  
**용도**: MarkText/Zettlr 호환 Mermaid 다이어그램 가이드  
**기준 환경**: MarkText, Zettlr (Mermaid v8.14.0)