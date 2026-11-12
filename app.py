import os
import streamlit as st
import requests
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()
API_BASE_URL = os.getenv("FRANKFURTER_API_URL", "https://api.frankfurter.dev/v1")

st.set_page_config(page_title="실시간 환율 조회기", page_icon="💱", layout="centered")

st.title("💱 실시간 환율 조회 웹앱")
st.caption("Frankfurter Exchange Rates API 기반")

# 1. 통화 목록 가져오기
@st.cache_data
def get_currencies():
    response = requests.get(f"{API_BASE_URL}/currencies")
    return response.json()

currencies = get_currencies()
currency_codes = list(currencies.keys())

# 2. 사용자 입력 UI 구성
col1, col2 = st.columns(2)
with col1:
    base_currency = st.selectbox("기준 통화 (From)", currency_codes, index=currency_codes.index("USD"))
with col2:
    target_currency = st.selectbox("대상 통화 (To)", currency_codes, index=currency_codes.index("KRW"))

amount = st.number_input("환전할 금액 입력", min_value=1.0, value=100.0, step=10.0)

# 3. 환율 조회 및 결과 출력
if st.button("환율 조회하기", use_container_width=True):
    if base_currency == target_currency:
        st.warning("기준 통화와 대상 통화가 같습니다.")
    else:
        res = requests.get(
            f"{API_BASE_URL}/latest",
            params={"amount": amount, "from": base_currency, "to": target_currency}
        )
        if res.status_code == 200:
            data = res.json()
            converted_amount = data["rates"][target_currency]
            date = data["date"]
            
            st.success(f"기준일: {date}")
            st.metric(
                label=f"{amount:,.2f} {base_currency} ({currencies[base_currency]})",
                value=f"{converted_amount:,.2f} {target_currency}"
            )
        else:
            st.error("환율 데이터를 불러오는 데 실패했습니다.")
            