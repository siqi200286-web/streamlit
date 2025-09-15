import streamlit as st
st.title(" Streamlit 과제 1")
A = st.number_input("숫자 A 입력", min_value=0, step=1)
B = st.number_input("숫자 B 입력", min_value=0, step=1)
if st.button("A + B 계산"):
  st.write(f" 결과: {A} + {B} = {A + B}")
  option = st.selectbox("A 또는 B 중 선택하세요", ["A", "B"])
if option == "A":
  total = sum(range(1, int(A) + 1))
  st.write(f"👉 1부터 A({A})까지의 합 = {total}")
  else:
  total = sum(range(1, int(B) + 1))
st.write(f"👉 1부터 B({B})까지의 합 = {total}")




