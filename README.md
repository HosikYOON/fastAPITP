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

<br>
<br>
--- SWAGGER ---

## USER
**POST CRATE User**
{
  "username": "hosik",
  "email": "hosik@naver.ocm",
  "name": "hosik",
  "password": "qwer1234"
}
<img width="894" height="778" alt="image" src="https://github.com/user-attachments/assets/7b98e1fe-fcc7-4df2-b404-cfe8b1b7992b" />

**POST Login** 
{
  "username": "hosik",
  "password": "qwer1234"
}

<img width="887" height="620" alt="image" src="https://github.com/user-attachments/assets/6f0c99f7-fb97-48ff-b03a-8aa9a3d0d056" />

**GET /users/**
<img width="887" height="634" alt="image" src="https://github.com/user-attachments/assets/9a5ffeb8-bef7-45a4-af60-216738e82029" />


**GET /users/{user_id}**
<img width="892" height="795" alt="image" src="https://github.com/user-attachments/assets/e0e3245c-4038-4e23-8134-86930f6becd2" />

PUT /users/{user_id}
user_id = 1
{
  "username": "hosikmodi",
  "email": "string",
  "password": "string",
  "name": "string"
}
<img width="885" height="736" alt="image" src="https://github.com/user-attachments/assets/f606bf5a-65b3-4b77-867c-dde4fa67b976" />


**DELETE /users/{user_id}**
user_id=1
<img width="886" height="910" alt="image" src="https://github.com/user-attachments/assets/1c0f6165-30fd-4658-95c6-e4ea978c9591" />

