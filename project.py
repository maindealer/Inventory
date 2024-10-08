import streamlit as st
import pandas as pd

st.title("📦재고관리 앱📦")

# 초기 데이터프레임 설정
initial_data = pd.DataFrame(
    [
        {"부품명": "", "개수": 0, "배송여부": False}
    ]
)

# 세션 상태에 초기화된 데이터가 없으면 기본값 설정
if 'data' not in st.session_state:
    st.session_state.data = initial_data

# CSV 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일 업로드", type='csv')

# 파일이 업로드되었을 때 세션 상태에 데이터 업데이트
if uploaded_file is not None:
    st.session_state.data = pd.read_csv(uploaded_file)
elif uploaded_file is None and 'uploaded' in st.session_state:
    # 파일이 제거된 경우 초기 데이터프레임으로 복원
    st.session_state.data = initial_data
    del st.session_state['uploaded']

# 파일이 업로드된 상태 저장
if uploaded_file:
    st.session_state['uploaded'] = True

# 데이터 수정 가능한 에디터
edited_df = st.data_editor(st.session_state.data)

# 부품 추가 기능
st.subheader("부품 추가")
부품명 = st.text_input("부품명", key='부품명')
개수 = st.number_input("개수", min_value=0, key='개수')
배송여부 = st.checkbox("배송여부", key='배송여부')

if st.button("부품 추가"):
    # 비어있는 행 찾기
    empty_row_index = st.session_state.data[st.session_state.data['부품명'] == ""].index

    if not empty_row_index.empty:
        # 비어있는 첫 번째 행에 추가
        first_empty_index = empty_row_index[0]
        st.session_state.data.at[first_empty_index, '부품명'] = 부품명
        st.session_state.data.at[first_empty_index, '개수'] = 개수
        st.session_state.data.at[first_empty_index, '배송여부'] = 배송여부
    else:
        # 비어있는 행이 없으면 새로운 행 추가
        new_row = pd.DataFrame({"부품명": [부품명], "개수": [개수], "배송여부": [배송여부]})
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

    st.success("부품이 추가되었습니다!")

# 최종 수정된 데이터프레임 표시
st.subheader("수정된 재고 리스트")
st.dataframe(st.session_state.data)

# 사용자로부터 파일명 입력받기
file_name = st.text_input("저장할 파일명", "재고리스트.csv")

# 수정된 데이터프레임을 CSV로 다운로드
if st.button("다운로드"):
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSV 다운로드",
        data=csv,
        file_name=file_name,
        mime='text/csv',
    )