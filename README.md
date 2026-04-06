# Medical Project

Flask 기반 건강 관리 데모 웹앱입니다.  
간단 설문, 상세 설문, 식단 이미지 업로드, 마이페이지 화면을 포함한 프로젝트입니다.

## Features

- 회원가입 / 로그인
- 건강 설문 입력
- 상세 설문 결과 확인
- 식단 이미지 업로드
- 마이페이지 조회
- 로컬 SQLite 기반 데모 실행

## Project Structure

```bash
.
├─ app.py
├─ requirements.txt
├─ templates/
└─ static/
```

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

실행 후 브라우저에서 아래 주소로 접속합니다.

```bash
http://localhost:5000
```

## Test Account

앱 실행 시 테스트 계정이 자동 생성됩니다.

- ID: `test`
- PW: `test123`

## Notes

- 이 저장소는 업로드용으로 정리된 버전입니다.
- 민감 정보, DB 파일, 노트북 파일, 모델 가중치, 업로드 결과물은 제외했습니다.
- 현재 일부 기능은 mock 데이터 기반으로 동작합니다.

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- SQLite
- HTML / CSS / JavaScript
- Pandas / NumPy
