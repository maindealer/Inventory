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
    st.session_state['uploaded'] = True
elif uploaded_file is None and 'uploaded' not in st.session_state:
    # 파일이 없을 때는 초기 데이터로 복원
    st.session_state.data = initial_data

# 데이터 수정 가능한 에디터
edited_df = st.data_editor(st.session_state.data)

# 부품 추가 기능
st.subheader("부품 추가")
부품명 = st.text_input("부품명", key='부품명')
개수 = st.number_input("개수", min_value=0, key='개수')
배송여부 = st.checkbox("배송여부", key='배송여부')

if st.button("부품 추가"):
    if 부품명 and 개수 > 0:
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
    else:
        st.warning("부품명과 개수를 확인하세요.")

# 최종 수정된 데이터프레임 표시
st.subheader("수정된 재고 리스트")
st.dataframe(st.session_state.data)

# 사용자로부터 파일명 입력받기
file_name = st.text_input("저장할 파일명", "재고리스트.csv")

# CSV 다운로드 버튼 먼저 표시
csv = st.session_state.data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="CSV 다운로드",
    data=csv,
    file_name=file_name,
    mime='text/csv',
)

# 저장 버튼 (필요시 별도의 동작 처리 가능)
if st.button("저장"):
    st.success(f"{file_name}으로 저장되었습니다!")
