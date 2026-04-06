# Health App Demo

정리된 Flask 데모 저장소입니다.

이 저장소는 원본 프로젝트에서 실행에 필요한 화면과 라우트만 추려 만든 업로드용 버전입니다.

## Included

- `app.py`
- `templates/`
- `static/`
- `requirements.txt`

## Excluded

- 로컬 DB 파일
- 노트북 파일
- 모델 가중치와 대용량 바이너리
- 서비스 계정 JSON, 키 파일, 업로드 결과물
- 실험용 하위 프로젝트와 가상환경

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

브라우저에서 `http://localhost:5000`으로 접속하면 됩니다.

기본 테스트 계정은 앱 실행 시 자동 생성됩니다.

- ID: `test`
- PW: `test123`

## Notes

- 현재 `app.py`는 데모용 mock 데이터와 로컬 SQLite를 사용합니다.
- GitHub 공개 저장소에 올릴 수 있도록 민감 정보와 불필요 산출물은 제외했습니다.
