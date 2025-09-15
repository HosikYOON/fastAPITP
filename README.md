# FASTAPI 팀 프로젝트

참가자 : 권혁준, 김진욱, 윤호식

간단한 모의 쇼핑몰 backend 프로젝트 입니다.

## 사전 조건

- uv 를 설치해 주세요
- mysql database 를 설정해주세요
  - "mall" user 를 만들어주고 password 를 12345 로 설정해주세요
  - 권한을 부여해주세요.

```sql
-- mall:12345 유저 생성
CREATE USER 'mall'@'localhost' IDENTIFIED BY '12345';
-- mall 유저에 권한 부여
GRANT ALL PRIVILEGES ON mall.* TO 'mall'@'localhost';
FLUSH PRIVILEGES;
-- mall DATABASE 생성
CREATE DATABASE mall;
```

(.env 파일은 원래 노출하지 않아야 하지만 학습용 프로젝트이기 때문에 포함시켰습니다.)

## 서버 시작 명령어

```bash
uv run uvicorn main:app --port 8081 --reload
```

## 확인용 Swagger UI 페이지

http://127.0.0.1:8081/docs

or

http://localhost:8081/docs

## USER
POST CRATE User
{
  "username": "hosik",
  "email": "hosik@naver.ocm",
  "name": "hosik",
  "password": "qwer1234"
}
<img width="894" height="778" alt="image" src="https://github.com/user-attachments/assets/7b98e1fe-fcc7-4df2-b404-cfe8b1b7992b" />


