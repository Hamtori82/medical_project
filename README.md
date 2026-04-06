
# Medical Project

건강 설문과 식단 이미지 업로드 기능을 통해 사용자 맞춤형 건강 정보를 제공하는 Flask 기반 웹 애플리케이션입니다.

## Overview

이 프로젝트는 사용자가 건강 상태를 더 쉽게 기록하고 확인할 수 있도록 기획한 건강 관리 데모 웹앱입니다.  
회원가입, 로그인, 건강 설문, 상세 설문 결과 확인, 식단 이미지 업로드, 마이페이지 기능을 포함하고 있습니다.

사용자 입력 흐름을 단순하게 구성하고, 설문과 이미지 업로드를 통해 건강 관리 서비스를 직관적으로 경험할 수 있도록 구현했습니다.

## Main Features

- 회원가입 / 로그인
- 건강 설문 입력
- 상세 건강 설문 결과 확인
- 식단 이미지 업로드
- 마이페이지 조회
- 로컬 SQLite 기반 데모 실행

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- SQLite
- HTML / CSS / JavaScript
- Pandas / NumPy

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

## My Contribution

- Flask 기반 웹앱 구조 정리 및 실행 가능한 형태로 프로젝트 재구성
- 설문 페이지와 상세 설문 페이지 라우팅 수정 및 흐름 개선
- 공개 저장소 업로드를 위해 불필요 파일과 민감 정보 정리
- `README`, `.gitignore` 등 문서와 저장소 구조 정리

## What I Learned

- Flask에서 라우팅과 템플릿 구조를 분리해 관리하는 방법
- 웹 프로젝트를 사용자 흐름 중심으로 정리하는 방법
- 공개 저장소 업로드 전 민감 정보와 불필요 파일을 정리하는 방법
- 기존 프로젝트를 다시 정돈해 포트폴리오 형태로 구성하는 방법

## Notes

- 이 저장소는 업로드용으로 정리된 버전입니다.
- 민감 정보, DB 파일, 노트북 파일, 모델 가중치, 업로드 결과물은 제외했습니다.
- 현재 일부 기능은 mock 데이터 기반으로 동작합니다.
