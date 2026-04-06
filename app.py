"""
생생건강통 - 웹 개발 학습용 버전
실제 동작하는 Flask 앱 with Mock 데이터

이 파일은 각 기능을 이해하면서 학습하기 위한 버전입니다.
실제 jimain.py는 너무 복잡하니, 여기서 단계별로 배워보세요!
"""

from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta
import os
import pandas as pd
import numpy as np

# ============================================
# 🔧 Flask 앱 초기화
# ============================================
app = Flask(__name__, static_url_path='/static')

# 앱 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_dev.db'
app.config['SECRET_KEY'] = 'dev-secret-key-change-me-in-production'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database 초기화
db = SQLAlchemy(app)
CORS(app)

# ============================================
# 📊 데이터베이스 모델
# ============================================
class User(db.Model):
    """사용자 계정 관리"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80))
    date = db.Column(db.String(80))  # 생년월일
    sex = db.Column(db.String(10))   # M / F
    password = db.Column(db.String(80))  # ⚠️ 실제로는 bcrypt 사용!
    
    def __init__(self, name, date, sex, username, password):
        self.username = username
        self.name = name
        self.password = password
        self.date = date
        self.sex = sex


# ============================================
# 🏠 라우트 1: 홈페이지
# ============================================
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    메인 진입점
    로그인 여부 체크해서 다른 페이지로 리다이렉트
    """
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('door.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    로그인된 사용자의 대시보드
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    username = session.get('name')
    return render_template('home.html', username=username)


# ============================================
# 🔐 라우트 2-4: 인증 (로그인/회원가입/로그아웃)
# ============================================
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    사용자 로그인
    
    GET: 로그인 페이지 표시
    POST: 사용자 검증 후 세션 설정
    """
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST: 로그인 처리
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        # DB에서 사용자 검색
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            # ✅ 로그인 성공
            session['logged_in'] = True
            session['name'] = username
            session['user_id'] = user.id
            return redirect('/home')
        else:
            # ❌ 로그인 실패
            return render_template('login.html', error='아이디 또는 비밀번호가 잘못되었습니다')
    except Exception as e:
        print(f"[ERROR] 로그인 실패: {str(e)}")
        return render_template('login.html', error='로그인 중 오류 발생')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """
    새 사용자 등록
    
    GET: 회원가입 페이지 표시
    POST: 새 사용자 DB에 저장
    """
    if request.method == 'GET':
        return render_template('register.html')
    
    # POST: 회원가입 처리
    try:
        new_user = User(
            name=request.form.get('name'),
            username=request.form.get('username'),
            date=request.form.get('date'),
            sex=request.form.get('sex', 'M'),
            password=request.form.get('password1')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/login/')
    except Exception as e:
        print(f"[ERROR] 회원가입 실패: {str(e)}")
        return render_template('register.html', error='회원가입 중 오류 발생')


@app.route('/logout', methods=['GET'])
def logout():
    """
    사용자 로그아웃
    세션 정보 삭제
    """
    session.clear()
    return redirect('/')


# ============================================
# 📋 라우트 5: 설문 조사
# ============================================
@app.route('/survey', methods=['GET'])
def survey():
    """
    건강 설문지 페이지
    간단한 기본 정보 입력
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    return render_template('simple_survey.html')


@app.route('/survey/detailed', methods=['GET'])
def detailed_survey():
    if not session.get('logged_in'):
        return redirect('/login/')

    return render_template('detailed_survey.html')


@app.route('/survey/result', methods=['GET', 'POST'])
def survey_result():
    """
    설문 제출 후 질병 예측
    
    📥 입력: 설문 응답값
    📤 출력: 질병별 확률
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    if request.method != 'POST':
        return redirect('/survey')
    
    try:
        # 1️⃣ 설문 데이터 수집 (설문지 HTML의 필드명에 맞게 수정)
        form_data = request.form
        
        print(f"[📝] 받은 설문 데이터: {dict(form_data)}")
        
        # 안전하게 필드 값 추출 (없으면 기본값 사용)
        def safe_float(field_name, default=0.0):
            value = form_data.get(field_name)
            try:
                result = float(value) if value else default
                print(f"  ✅ {field_name}: {result}")
                return result
            except (ValueError, TypeError) as e:
                print(f"  ⚠️ {field_name}: 변환 오류 ({value}) -> 기본값 {default} 사용")
                return default
        
        def safe_int(field_name, default=1):
            value = form_data.get(field_name)
            try:
                result = int(value) if value else default
                print(f"  ✅ {field_name}: {result}")
                return result
            except (ValueError, TypeError) as e:
                print(f"  ⚠️ {field_name}: 변환 오류 ({value}) -> 기본값 {default} 사용")
                return default
        
        # 각 필드를 안전하게 추출
        survey_dict = {
            'AGE': safe_float('AGE', 35),
            'SEX': safe_int('SEX', 1),
            'HE_HT': safe_float('HE_HT', 170),
            'HE_WT': safe_float('HE_WT', 65),
            'HE_DBP': safe_float('HE_DBP', 80),
            'TOTAL_SLP_WD': safe_float('TOTAL_SLP_WD', 7),
            'LQ_3EQL': safe_float('LQ_3EQL', 1),
            'LQ_1EQL': safe_int('LQ_1EQL', 1),
            'LQ_2EQL': safe_int('LQ_2EQL', 1),
            'LQ_4EQL': safe_int('LQ_4EQL', 1),
            'LQ_5EQL': safe_int('LQ_5EQL', 1),
            'BE3_81': safe_int('BE3_81', 1),
            'BE3_85': safe_int('BE3_85', 1),
            'BP1': safe_int('BP1', 1),
            'SM_PRESNT': safe_int('SM_PRESNT', 0),
            'L_BR_FQ': safe_int('L_BR_FQ', 1),
            'BH1': safe_int('BH1', 1),
            'HE_FH': safe_int('HE_FH', 0),
        }
        
        survey_data = pd.DataFrame({k: [v] for k, v in survey_dict.items()})

        # 2️⃣ Mock 질병 예측 결과 (실제로는 20개 ML 모델 실행)
        disease_predictions = {
            '당뇨병2형': round(np.random.uniform(30, 80), 1),
            '당뇨병3형': round(np.random.uniform(20, 60), 1),
            '고혈압1단계': round(np.random.uniform(25, 65), 1),
            '고혈압2단계': round(np.random.uniform(15, 50), 1),
            '고지혈증': round(np.random.uniform(20, 55), 1),
            '뇌졸중': round(np.random.uniform(10, 40), 1),
            '심근경색': round(np.random.uniform(15, 45), 1),
            '골다공증': round(np.random.uniform(20, 50), 1),
            '만성신질환': round(np.random.uniform(5, 35), 1),
            '폐쇄성수면무호흡증': round(np.random.uniform(15, 55), 1),
        }

        # 3️⃣ 결과를 DB에 저장
        username = session.get('name')
        print(f"\n[✅] {username}님의 설문 데이터 처리 완료!")
        print(f"[✅] 예측 결과: {disease_predictions}\n")

        # 4️⃣ 결과 페이지로 이동
        return render_template(
            'survey_result.html',
            survey_data=survey_data,
            predictions=disease_predictions
        )
        
    except Exception as e:
        import traceback
        print(f"\n[❌] 설문 처리 오류: {str(e)}")
        print(f"[❌] 상세 오류:\n{traceback.format_exc()}\n")
        error_msg = f'설문 처리 중 오류가 발생했습니다. 관리자에게 문의해주세요.'
        return render_template('error.html', message=error_msg, error_details=str(e))


# ============================================
# 🔄 라우트 5-2: 상세 설문 결과
# ============================================
@app.route('/survey/detailed/result', methods=['POST'])
def detailed_survey_result():
    """
    상세 설문 결과 처리
    
    POST: 상세 설문 폼 데이터 받기
    - simple survey보다 더 많은 필드 (+15개)
    - 더 상세한 결과 페이지 렌더링
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    try:
        form_data = request.form.to_dict()
        print(f"\n[📋] 상세 설문 데이터 처리 시작")
        print(f"[📊] 받은 상세 필드 수: {len(form_data)}")
        
        # 1️⃣ Safe한 필드 파싱
        def safe_float(field_name, default=0.0):
            value = form_data.get(field_name)
            try:
                result = float(value) if value else default
                return result
            except (ValueError, TypeError):
                return default
        
        def safe_int(field_name, default=0):
            value = form_data.get(field_name)
            try:
                result = int(value) if value else default
                return result
            except (ValueError, TypeError):
                return default
        
        survey_dict = {
            'SEX': safe_int('SEX', 1),
            'AGE': safe_int('AGE', 50),
            'HE_HT': safe_float('HE_HT', 170),
            'HE_WT': safe_float('HE_WT', 65),
            'HE_DBP': safe_float('HE_DBP', 80),
            'TOTAL_SLP_WD': safe_float('TOTAL_SLP_WD', 7),
            'LQ_1EQL': safe_int('LQ_1EQL', 1),
            'LQ_2EQL': safe_int('LQ_2EQL', 1),
            'LQ_3EQL': safe_int('LQ_3EQL', 1),
            'LQ_4EQL': safe_int('LQ_4EQL', 1),
            'LQ_5EQL': safe_int('LQ_5EQL', 1),
            'BE3_81': safe_int('BE3_81', 1),
            'BE3_85': safe_int('BE3_85', 1),
            'BP1': safe_int('BP1', 1),
            'SM_PRESNT': safe_int('SM_PRESNT', 0),
            'L_BR_FQ': safe_int('L_BR_FQ', 1),
            'BH1': safe_int('BH1', 1),
            'HE_FH': safe_int('HE_FH', 0),
            'MH_STRESS': safe_int('MH_STRESS', 0),
            'N_INTK': safe_float('N_INTK', 0),
            'N_EN': safe_float('N_EN', 0),
            'N_PROT': safe_float('N_PROT', 0),
            'N_FAT': safe_float('N_FAT', 0),
            'N_SUGAR': safe_float('N_SUGAR', 0),
        }
        
        survey_data = pd.DataFrame({k: [v] for k, v in survey_dict.items()})
        
        # 2️⃣ Mock 질병 예측 결과 (상세 버전 - 더 정교한 예측)
        disease_predictions = {
            '당뇨병2형': round(np.random.uniform(30, 80), 1),
            '당뇨병3형': round(np.random.uniform(20, 60), 1),
            '고혈압1단계': round(np.random.uniform(25, 65), 1),
            '고혈압2단계': round(np.random.uniform(15, 50), 1),
            '고지혈증': round(np.random.uniform(20, 55), 1),
            '뇌졸중': round(np.random.uniform(10, 40), 1),
            '심근경색': round(np.random.uniform(15, 45), 1),
            '골다공증': round(np.random.uniform(20, 50), 1),
            '만성신질환': round(np.random.uniform(5, 35), 1),
            '폐쇄성수면무호흡증': round(np.random.uniform(15, 55), 1),
        }
        
        # 3️⃣ 결과를 DB에 저장
        username = session.get('name')
        print(f"\n[✅] {username}님의 상세 설문 데이터 처리 완료!")
        print(f"[✅] 예측 결과: {disease_predictions}\n")
        
        age = survey_dict['AGE']
        sex = survey_dict['SEX']
        height = survey_dict['HE_HT']
        weight = survey_dict['HE_WT']
        sleep = survey_dict['TOTAL_SLP_WD']
        
        # 4️⃣ 상세 결과 페이지로 이동
        return render_template(
            'detailed_survey_result.html',
            predictions=disease_predictions,
            age=age,
            sex=sex,
            height=height,
            weight=weight,
            sleep=sleep
        )
        
    except Exception as e:
        import traceback
        print(f"\n[❌] 상세 설문 처리 오류: {str(e)}")
        print(f"[❌] 상세 오류:\n{traceback.format_exc()}\n")
        error_msg = f'상세 설문 처리 중 오류가 발생했습니다. 관리자에게 문의해주세요.'
        return render_template('error.html', message=error_msg, error_details=str(e))


# ============================================
# 🍽️ 라우트 6: 음식 탐지
# ============================================
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    이미지 업로드 페이지
    
    GET: 이미지 업로드 폼 표시
    POST: 이미지 업로드 받기 (아직 탐지 안 함)
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    if request.method == 'GET':
        return render_template('detect.html')
    
    # POST: 이미지 파일 받기
    if 'file' not in request.files:
        return render_template('detect.html', error='파일을 선택해주세요')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('detect.html', error='파일을 선택해주세요')
    
    try:
        # 파일 저장
        filename = f"food_{session.get('user_id')}.jpg"
        filepath = os.path.join('static', 'uploads', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        
        print(f"[✅] 이미지 업로드: {filepath}")
        return redirect(f'/predict/result?image={filename}')
        
    except Exception as e:
        print(f"[❌] 이미지 업로드 오류: {str(e)}")
        return render_template('detect.html', error='이미지 업로드 실패')


@app.route('/predict/result', methods=['GET', 'POST'])
def predict_result():
    """
    YOLOv5 음식 탐지 결과
    
    📥 입력: 이미지 파일
    📤 출력: 탐지된 음식 목록 + 영양정보
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    try:
        image_file = request.args.get('image', 'unknown')
        
        # Mock: YOLOv5 탐지 결과
        detected_foods = [
            {'name': '쌀밥', 'confidence': 0.92, 'nutrition': {'calories': 206, 'carbs': '45g'}},
            {'name': '계란후라이', 'confidence': 0.87, 'nutrition': {'calories': 162, 'protein': '13g'}},
            {'name': '된장찌개', 'confidence': 0.79, 'nutrition': {'calories': 65, 'protein': '6g'}},
        ]
        
        # 영양정보 합계 계산
        nutrition_total = {
            'calories': 206 + 162 + 65,
            'carbs': '45g',
            'protein': '13g + 6g = 19g',
            'fat': '-'
        }
        
        print(f"[✅] 음식 탐지 완료: {len(detected_foods)}개 항목")
        
        return render_template(
            'food_result.html',
            detected_foods=detected_foods,
            nutrition_total=nutrition_total,
            image_file=image_file
        )
        
    except Exception as e:
        print(f"[❌] 음식 탐지 오류: {str(e)}")
        error_msg = f'음식 탐지 중 오류 발생: {str(e)}'
        return render_template('error.html', message=error_msg)


# ============================================
# 🍽️ 라우트 6-2: 음식 탐지 (상세 결과)
# ============================================
@app.route('/predict/result/detailed', methods=['GET'])
def predict_result_detailed():
    """
    상세 음식 탐지 결과
    
    각 음식별 O/X 라벨링 포함
    - O: 권장 음식 (채소, 생선, 저지방 단백질)
    - X: 비권장 음식 (고지방, 고염분)
    - ○: 보통 (적당량 섭취 권장)
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    try:
        image = request.args.get('image', None)
        
        # Mock: YOLOv5 탐지 결과 (건강도 평가 포함)
        foods = [
            {
                'name': '쌀밥',
                'confidence': 0.92,
                'healthiness': 'neutral'  # 보통 - 적당량 권장
            },
            {
                'name': '계란후라이',
                'confidence': 0.87,
                'healthiness': 'bad'  # X - 높은 지방함량
            },
            {
                'name': '된장찌개',
                'confidence': 0.79,
                'healthiness': 'good'  # O - 영양가 높고 염분만 주의
            },
        ]
        
        # 총 영양정보 (Mock)
        total_nutrition = {
            'calories': 433,  # 206 + 162 + 65
            'carbs': 55.2,    # 탄수화물
            'protein': 25.0,  # 단백질
            'fat': 15.8,      # 지방
        }
        
        print(f"\n[✅] 상세 음식 탐지 완료: {len(foods)}개 항목")
        print(f"[✅] 영양정보: {total_nutrition}\n")
        
        return render_template(
            'food_result_detailed.html',
            foods=foods,
            image=image,
            calories=total_nutrition['calories'],
            carbs=total_nutrition['carbs'],
            protein=total_nutrition['protein'],
            fat=total_nutrition['fat']
        )
        
    except Exception as e:
        import traceback
        print(f"\n[❌] 상세 음식 탐지 오류: {str(e)}")
        print(f"[❌] 상세 오류:\n{traceback.format_exc()}\n")
        error_msg = f'상세 분석 중 오류 발생'
        return render_template('error.html', message=error_msg, error_details=str(e))


# ============================================
# 👤 라우트 7: 마이페이지
# ============================================
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    """
    사용자 프로필 및 통계
    
    - 사용자 정보 표시
    - 질병 예측 히스토리
    - 식단 기록
    """
    if not session.get('logged_in'):
        return redirect('/login/')
    
    username = session.get('name')
    user = User.query.filter_by(username=username).first()
    
    # Mock 데이터
    prediction_history = [
        {'date': '2024-04-01', 'disease': '당뇨병', 'probability': 65},
        {'date': '2024-03-15', 'disease': '고혈압', 'probability': 45},
    ]
    
    meal_history = [
        {'date': '2024-04-05', 'foods': ['쌀밥', '계란후라이'], 'calories': 400},
        {'date': '2024-04-04', 'foods': ['비빔밥', '미역국'], 'calories': 520},
    ]
    
    # Chart 데이터 준비
    # 1️⃣ 질병 예측 차트 (수평 막대)
    labels = ['당뇨병2형', '고혈압', '이상지질혈증', '비만', '만성폐질환', 
              '관절염', '우울증', '심장질환', '뇌졸중', '암']
    data = [round(np.random.uniform(20, 80), 1) for _ in range(10)]
    
    # 2️⃣ 영양소 비율 차트 (도넛)
    nutrient_labels = ['탄수화물', '단백질', '지방']
    nutrient_data = [
        round(np.random.uniform(45, 65), 1),  # 탄수화물 %
        round(np.random.uniform(10, 25), 1),  # 단백질 %
        round(np.random.uniform(15, 35), 1)   # 지방 %
    ]
    
    return render_template(
        'mypage.html',
        user=user,
        prediction_history=prediction_history,
        meal_history=meal_history,
        labels=labels,
        data=data,
        nutrient_labels=nutrient_labels,
        nutrient_data=nutrient_data
    )


# ============================================
# 📡 API 엔드포인트 (iOS 앱 연동용 - 나중에)
# ============================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    서버 상태 확인 (for iOS app)
    """
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'message': '서버가 정상 작동 중입니다'
    })


# ============================================
# 🚀 서버 실행
# ============================================
if __name__ == '__main__':
    # DB 초기화
    with app.app_context():
        db.create_all()
        
        # 테스트 사용자 추가
        test_user = User.query.filter_by(username='test').first()
        if not test_user:
            test_user = User(
                name='테스트 사용자',
                username='test',
                date='1990-01-01',
                sex='M',
                password='test123'
            )
            db.session.add(test_user)
            db.session.commit()
            print("[✅] 테스트 사용자 생성: test / test123")
    
    # 🚀 Flask 서버 시작
    print("""
    ╔════════════════════════════════════════╗
    ║   🚀 생생건강통 (개발 버전) 시작!      ║
    ╚════════════════════════════════════════╝
    
    📍 접속 주소: http://localhost:5000
    
    🧪 테스트 계정:
       - 아이디: test
       - 비밀번호: test123
    
    💡 팁:
       1. 회원가입 후 로그인 시도
       2. 설문 작성 후 질병 예측 결과 확인  
       3. 이미지 업로드해서 음식 탐지
       4. 마이페이지에서 히스토리 확인
    
    ⚠️  개발 모드 (디버그 활성화)
    """)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
