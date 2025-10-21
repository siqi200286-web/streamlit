import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 페이지 기본 설정
st.set_page_config(page_title="지능형 신용평가(Logit)", page_icon="6688", layout="wide")
st.title(" 지능형 신용평가 모형 (로지스틱 회귀)")

# 저장된 모델 불러오기
pipe = joblib.load("pipeline.joblib")

# 수치형 변수 목록
NUM = ["loan_amnt","term","int_rate","annual_inc","dti","emp_length","revol_util",
       "open_acc","total_acc","inq_last_6mths","delinq_2yrs","revol_bal","pub_rec"]

# 범주형 변수 목록
CAT = ["home_ownership","purpose","grade","sub_grade","verification_status","addr_state"]

# ------------------------------------------------------------------
#  개별 예측
# ------------------------------------------------------------------
st.subheader(" 개별 예측 (단일 고객 입력)")

cols = st.columns(3)
vals = {}

# 수치형 입력값
for i, c in enumerate(NUM):
    with cols[i % 3]:
        default = 10000.0 if c == "loan_amnt" else 0.0
        vals[c] = st.number_input(c, value=default)

# 범주형 입력값
for i, c in enumerate(CAT):
    with cols[i % 3]:
        default_text = (
            "A1" if c == "sub_grade"
            else "RENT" if c == "home_ownership"
            else "CA" if c == "addr_state"
            else "Verified"
        )
        vals[c] = st.text_input(c, default_text)

# 예측 버튼 클릭 시 결과 출력
if st.button("예측 실행"):
    x = pd.DataFrame([vals])
    for c in NUM + CAT:
        if c not in x:
            x[c] = np.nan

    p_bad = float(pipe.predict_proba(x)[:, 1][0])
    st.metric("부실 확률(p_bad)", f"{p_bad:.3f}")
    st.write("신용 판정 결과:", " 부실(1)" if p_bad >= 0.5 else " 건전(0)")

# ------------------------------------------------------------------
#  CSV 파일 일괄 예측
# ------------------------------------------------------------------
st.subheader(" CSV 일괄 예측")
st.caption("업로드된 CSV 파일은 학습 시 사용한 변수 이름과 동일해야 합니다.")

up = st.file_uploader("CSV 파일 업로드", type="csv")

if up is not None:
    df = pd.read_csv(up)

    # 누락된 열이 있을 경우 채워 넣기
    for c in NUM + CAT:
        if c not in df:
            df[c] = np.nan

    X = df[NUM + CAT]
    prob = pipe.predict_proba(X)[:, 1]
    out = df.copy()
    out["p_bad"] = prob
    out["pred"] = (out["p_bad"] >= 0.5).astype(int)

    st.dataframe(out.head(20))

    st.download_button(
        "결과 다운로드 (CSV)",
        out.to_csv(index=False).encode("utf-8"),
        file_name="predictions.csv",
        mime="text/csv",
    )




