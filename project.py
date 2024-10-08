import streamlit as st
import pandas as pd

st.title("📦재고관리 앱📦")

# 초기 데이터프레임
df = pd.DataFrame(
    [
        {"부품명": "", "개수": 0, "배송여부": False}
    ]
)

# CSV 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일 업로드", type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# 데이터 수정 가능한 에디터
edited_df = st.data_editor(df)

# 부품 추가 기능
st.subheader("부품 추가")
부품명 = st.text_input("부품명")
개수 = st.number_input("개수", min_value=0)
배송여부 = st.checkbox("배송여부")

if st.button("부품 추가"):
    new_row = pd.DataFrame({"부품명": [부품명], "개수": [개수], "배송여부": [배송여부]})
    edited_df = pd.concat([edited_df, new_row], ignore_index=True)
    st.success("부품이 추가되었습니다!")

# 최종 수정된 데이터프레임 표시
st.subheader("수정된 재고 리스트")
st.dataframe(edited_df)

# 사용자로부터 파일명 입력받기
file_name = st.text_input("저장할 파일명", "재고리스트.csv")

# 수정된 데이터프레임을 CSV로 다운로드
if st.button("CSV로 다운로드"):
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSV 다운로드",
        data=csv,
        file_name=file_name,
        mime='text/csv',
    )