# MJSEC_BOJ

MJSEC 프로그래밍 대회를 위한 알고리즘 플랫폼입니다.

해당 사이트는 Solved.ac API를 활용하여 만들었습니다.

---

## 목차
1. [Docker를 이용한 서버 구축](#docker를-이용한-서버-구축)
2. [관리자 계정 생성](#관리자-계정-생성)
3. [대회 설정 방법](#대회-설정-방법)
4. [문제 해결](#문제-해결)

---

## Docker를 이용한 서버 구축

### 사전 요구사항

- Docker 설치
- Docker Compose 설치

### 1. 환경 변수 설정

`boj_contest/.env` 파일을 생성하고 다음 내용을 설정하세요:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### 2. Docker Compose로 서버 실행

```bash
cd boj_contest

# Docker 이미지 빌드 및 컨테이너 실행
docker-compose up -d --build
```

이 명령어는 다음을 자동으로 수행합니다:
- Django 애플리케이션 빌드 (Python 3.11 기반)
- 데이터베이스 마이그레이션 (`migrate`)
- 정적 파일 수집 (`collectstatic`)
- Gunicorn으로 Django 서버 실행 (포트 8000)
- Nginx 웹 서버 실행 (포트 80, 443)

### 3. 서비스 확인

- **HTTP**: `http://localhost:80`
- **HTTPS**: `https://localhost:443` (SSL 인증서 설정 필요)
- **Django 직접 접근**: `http://localhost:8000`

### 4. Docker 로그 확인

```bash
# 모든 서비스 로그 실시간 확인
docker-compose logs -f

# Django 웹 서버 로그만 확인
docker-compose logs -f web

# Nginx 로그만 확인
docker-compose logs -f nginx
```

### 5. Docker 컨테이너 관리

```bash
# 컨테이너 중지
docker-compose stop

# 컨테이너 중지 및 삭제
docker-compose down

# 컨테이너 재시작
docker-compose restart

# 볼륨까지 모두 삭제 (데이터 초기화)
docker-compose down -v
```

---

## 관리자 계정 생성

Django 관리자 페이지(`/admin`)에 접근하기 위한 슈퍼유저를 생성합니다:

```bash
docker-compose exec web python manage.py createsuperuser
```

프롬프트에 따라 입력:
- Username (사용자명)
- Email address (이메일)
- Password (비밀번호, 2번 입력)

관리자 계정 생성 후 `http://localhost/admin`에서 로그인하세요.

---

## 대회 설정 방법

### 1. 관리자 페이지 접속

`http://localhost/admin`으로 접속하여 슈퍼유저 계정으로 로그인합니다.

### 2. 대회 생성

1. 좌측 메뉴에서 **Competitions** 클릭
2. **Add Competition** 버튼 클릭
3. 대회 정보 입력:
   - 대회 이름
   - 시작 시간
   - 종료 시간
   - 설명
4. **Save** 버튼 클릭

### 3. 참가자 등록

1. 좌측 메뉴에서 **Participants** 클릭
2. **Add Participant** 버튼 클릭
3. 참가자 정보 입력:
   - 사용자 계정 선택 또는 생성
   - Solved.ac 핸들(아이디) 입력 **필수**
   - 소속 대회 선택
4. **Save** 버튼 클릭

### 4. 문제 등록

1. 좌측 메뉴에서 **Contest Problems** 클릭
2. **Add Contest Problem** 버튼 클릭
3. 문제 정보 입력:
   - 소속 대회 선택
   - 백준 문제 번호 (problem_id)
   - 배점 (points)
   - 문제 제목 (선택)
4. **Save** 버튼 클릭

---

## 문제 해결

### 포트 충돌 오류

80 또는 443 포트가 이미 사용 중이면 `docker-compose.yml` 파일에서 포트를 변경하세요:

```yaml
nginx:
  ports:
    - "8080:80"    # 80 대신 8080 사용
    - "8443:443"   # 443 대신 8443 사용
```

### 정적 파일이 로드되지 않을 때

```bash
# 컨테이너 내에서 정적 파일 재수집
docker-compose exec web python manage.py collectstatic --noinput

# 서비스 재시작
docker-compose restart
```

### 데이터베이스 초기화

```bash
# 컨테이너와 볼륨 모두 삭제
docker-compose down -v

# 다시 빌드 및 실행
docker-compose up -d --build

# 관리자 계정 재생성 필요
docker-compose exec web python manage.py createsuperuser
```

### SSL/HTTPS 인증서 설정

#### 1. 인증서 파일 준비

인증서 파일을 `boj_contest/certs/` 디렉토리에 배치합니다:

```bash
cd boj_contest
mkdir -p certs

# 인증서 파일 복사 (파일명은 nginx 설정에 맞춰야 함)
# 현재 설정 기준:
# - boj.mjsec.kr.crt (인증서 파일)
# - boj.mjsec.kr.key (개인키 파일)
```

**필요한 파일:**
- `boj.mjsec.kr.crt` - SSL 인증서 (또는 `.pem`, `.cert`)
- `boj.mjsec.kr.key` - 개인키 파일

#### 2. Nginx 설정 확인

`nginx/default.conf` 파일에서 인증서 경로를 확인하세요:

```nginx
ssl_certificate     /etc/nginx/certs/boj.mjsec.kr.crt;
ssl_certificate_key /etc/nginx/certs/boj.mjsec.kr.key;
```

**인증서 파일명이 다를 경우** `nginx/default.conf`를 수정:

```nginx
ssl_certificate     /etc/nginx/certs/your-cert.crt;
ssl_certificate_key /etc/nginx/certs/your-key.key;
```

#### 3. 도메인 설정

`nginx/default.conf`에서 `server_name`을 실제 도메인으로 변경:

```nginx
server_name boj.mjsec.kr;  # 실제 도메인으로 변경
```

#### 4. Let's Encrypt 무료 인증서 사용 (선택)

Let's Encrypt를 사용하는 경우:

```bash
# Certbot 설치 후
sudo certbot certonly --standalone -d boj.mjsec.kr

# 생성된 인증서를 certs 디렉토리로 복사
sudo cp /etc/letsencrypt/live/boj.mjsec.kr/fullchain.pem ./certs/boj.mjsec.kr.crt
sudo cp /etc/letsencrypt/live/boj.mjsec.kr/privkey.pem ./certs/boj.mjsec.kr.key
```

#### 5. 컨테이너 재시작

인증서 설정 후 컨테이너를 재시작합니다:

```bash
docker-compose restart nginx
```

**주의:** `certs/` 디렉토리는 `.gitignore`에 추가하여 인증서가 Git에 커밋되지 않도록 하세요!

---

## 기술 스택

- **Backend**: Django 5.1
- **WSGI Server**: Gunicorn 20.1.0
- **Web Server**: Nginx (latest)
- **Database**: SQLite (개발/소규모), PostgreSQL 권장 (대규모)
- **Container**: Docker + Docker Compose
- **Python**: 3.11

---

## 디렉토리 구조

```
MJSEC_BOJ/
└── boj_contest/
    ├── docker-compose.yml    # Docker Compose 설정
    ├── dockerfile            # Django 컨테이너 빌드 설정
    ├── requirements.txt      # Python 패키지 목록
    ├── manage.py            # Django 관리 명령어
    ├── boj_contest/         # Django 프로젝트 설정
    ├── competition/         # 대회 앱
    ├── nginx/               # Nginx 설정 파일
    ├── certs/               # SSL 인증서 디렉토리
    ├── static/              # 정적 파일
    ├── media/               # 미디어 파일
    └── .env                 # 환경 변수 (생성 필요)
```
