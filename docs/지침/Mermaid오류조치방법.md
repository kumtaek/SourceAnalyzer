# Mermaid 오류 조치방법

## 개요
본 문서는 Mermaid 다이어그램 작성 시 발생하는 오류들과 해결방법을 정리한 가이드입니다. 실제 개발 환경에서 발생한 문제들을 바탕으로 작성되었습니다.

## Mermaid Invalid Codes 체크리스트

### 1. HTML 태그 오인식 방지

**문제**: `<User>` 같은 표기는 HTML 태그로 인식되어 오류 발생

**해결**: HTML 엔티티 사용

```mermaid
# ❌ 잘못된 예
A[<User> 정보] --> B[처리]

# ✅ 올바른 예  
A[&lt;User&gt; 정보] --> B[처리]
```

### 2. 줄바꿈 처리 (환경별 대응)

#### 기본 원칙 (표준 Mermaid):
- **노드 라벨 안** ([], {}, ()) → `\n` 은 줄바꿈으로 동작
- **노드 라벨 밖** (예: style, 일반 텍스트) → `\n` 그대로 출력
- ✅ **권장**: 라벨 안 줄바꿈은 `\n` 사용

#### 환경별 예외 처리:
- **MarkText, 구버전 Mermaid**: `\n`이 동작하지 않는 경우 발생
- **복잡한 라벨**: 한글 + 숫자 + 특수문자 조합 시 `\n` 실패 가능
- **HTML 태그 혼재**: 다른 HTML 태그와 함께 사용 시 충돌

#### 해결 방법 우선순위:

```mermaid
# 1순위: 표준 방법 (권장)
A["첫 번째 줄\n두 번째 줄"]

# 2순위: \n 동작 안 할 때
A["첫 번째 줄<br/>두 번째 줄"]

# 3순위: 복잡한 경우
A["복잡한 내용<br/>특수문자 &lt;tag&gt;<br/>여러 줄"]
```

**실제 적용 예시**:
```mermaid
# ❌ 동작하지 않는 경우
JSP["JSP Pages\n12개 파일"]

# ✅ 해결된 경우
JSP["JSP Pages<br/>12개 파일"]
```

### 3. 긴 라벨 / 특수문자

**문제**: 라벨이 길거나 `{}`, `<`, `>` 같은 특수문자가 포함되면 파싱 오류 위험 ↑

**해결**: 라벨을 `[" ... "]` 로 감싸기

```mermaid
# ❌ 위험한 예
A[UserController{복잡한내용}] --> B

# ✅ 안전한 예
A["UserController{복잡한내용}"] --> B
```

### 4. 이모지 사용

**문제**: 일부 이모지(✅, ❌, 🔄)는 파서에서 깨짐

**해결**: "✔", "✗" 같은 단순 기호 사용

```mermaid
# ❌ 문제 발생 가능
A[처리 완료 ✅] --> B[다음 단계 🔄]

# ✅ 안전한 방법
A[처리 완료 ✔] --> B[다음 단계 →]
```

### 5. 중복 정의

**문제**: 
- 같은 edge(예: A --> B)를 두 번 선언 → 오류
- 같은 style을 두 번 선언 → 경고/혼란

**해결**: 중복 제거

```mermaid
# ❌ 중복 정의
A --> B
A --> B  # 중복!
style A fill:#red
style A fill:#blue  # 중복!

# ✅ 중복 제거
A --> B
style A fill:#red
```

### 6. ERD(erDiagram) 제약

**문제**: 
- PK/FK, 제약조건, 인덱스 → 지원 안 됨
- 복잡한 속성 정의 → 파싱 오류

**지원되는 형식**:
- 속성 정의: `string name`, `int age` 같은 단순 형식만 지원
- 관계 정의: `A ||--o{ B : has` 형태만 지원

**해결**: 단순 문법만 사용

```mermaid
# ✅ 지원되는 ERD 문법
erDiagram
    USER {
        string name
        int age
        string email
    }
    ORDER {
        int order_id
        string status
    }
    USER ||--o{ ORDER : has

# ❌ 지원되지 않는 문법
USER {
    string name PK
    int age NOT NULL
    string email UNIQUE
}
```

### 7. 클래스 다이어그램 제약

**문제**: 복잡한 타입 정의나 관계는 파싱 오류 발생

**해결**: 단순 문법만 사용

```mermaid
# ❌ 복잡한 정의
class User {
    +String getName()
    +void setName(String name)
}
User ||--o{ Order

# ✅ 단순 정의
class User {
    +name
    +age
    +getName()
    +setName()
}
User --> Order
```

### 8. 초기화 블록(init)

**문제**: JSON은 큰따옴표만 허용

```mermaid
# ❌ 작은따옴표 사용
%%{init: {'theme':'default'}}%%

# ✅ 큰따옴표 사용
%%{init: {"theme":"default"}}%%
```

### 9. 화살표 기호

**문제**: 유니코드 화살표 `→`는 지원되지 않음

**해결**: `->` 사용

```mermaid
# ❌ 유니코드 화살표
A → B

# ✅ ASCII 화살표
A -> B
A --> B
```

## 환경별 대응 가이드

### MarkText 사용 시
- `\n` 대신 `<br/>` 태그 우선 사용
- 복잡한 한글 라벨은 반드시 큰따옴표로 감싸기
- 특수문자 포함 시 HTML 엔티티 사용

### VS Code + Mermaid Extension
- 표준 `\n` 문법 정상 동작
- 실시간 미리보기에서 오류 확인 가능

### GitHub/GitLab
- 표준 Mermaid 문법 지원
- 이모지 지원 제한적

## 다이어그램 타입별 특수 규칙

### 시퀀스 다이어그램
- **participant 식별자**: 영문만 사용 (한글 사용 시 오류)
- **표시명**: `as` 키워드로 한글 지정 가능
- **메시지/노트**: 한글 사용 가능

```mermaid
# ✅ 올바른 시퀀스 다이어그램
sequenceDiagram
    participant U as 사용자
    participant S as 시스템
    U->>S: 로그인 요청
    Note over S: 인증 처리
    S-->>U: 로그인 완료

# ❌ 잘못된 예 (participant에 한글)
sequenceDiagram
    participant 사용자
    participant 시스템
```

**핵심 규칙**:
- ✅ 메시지 텍스트: 한글 가능
- ✅ 노트 내용: 한글 가능
- ✅ as 뒤 표시명: 한글 가능
- ❌ participant 식별자: 영문만 가능
- ❌ 변수/함수명: 영문만 가능

### 클래스 다이어그램
- `+String name` → `+name` (타입 제거)
- `||--o{` → `-->` (단순 관계)
- 메서드/속성은 단순 문자열만 허용

## 지원/미지원 다이어그램

### ✅ 지원되는 다이어그램:
- flowchart/graph ✅
- sequenceDiagram ✅
- pie chart ✅
- state diagram ✅
- classDiagram ✅ 

### ❌ 미지원 다이어그램:
- quadrantChart (v9+ 신기능)
- timeline (v9+ 신기능)
- mindmap (v9+ 신기능)
- gitgraph

## 디버깅 방법

### 1. 단계별 축소
복잡한 다이어그램에서 오류 발생 시:
1. 노드 하나씩 제거하면서 테스트
2. 오류 발생 지점 특정
3. 해당 부분만 수정

### 2. 브라우저 개발자 도구 활용
- F12 → Console 탭에서 Mermaid 오류 메시지 확인
- 구체적인 파싱 오류 위치 파악 가능

### 3. 온라인 Mermaid 에디터 활용
- https://mermaid.live/ 에서 테스트
- 실시간으로 오류 확인 및 수정

## 최종 요약

### ✅ 안전한 작성법
1. HTML 태그: `&lt;tag&gt;` 사용
2. 줄바꿈: `\n` 우선, 안되면 `<br/>` 사용  
3. 긴 라벨: `"내용"` 큰따옴표로 감싸기
4. 이모지: 단순 기호 사용 (`✔`, `✗`)
5. 중복: 관계/스타일 중복 제거
6. ERD: 단순 문법만 사용 (PK/FK 불가)
7. init: 큰따옴표 JSON (`{"theme":"default"}`)
8. 화살표: `->` 사용 (유니코드 `→` 금지)

### 🔧 문제 해결 순서
1. **기본 문법 확인**: 표준 Mermaid 문법 준수
2. **환경 확인**: 사용 중인 뷰어/에디터 특성 파악
3. **단계적 수정**: 복잡한 부분부터 단순화
4. **테스트**: 온라인 에디터에서 검증
5. **적용**: 실제 환경에 반영
