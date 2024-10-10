import streamlit as st
import pandas as pd

st.title("📦재고관리 앱📦")

# CSV 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일 업로드", type='csv')

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["전체 재고", "보유함", "구매 예정", "배송 중"])

# 전체 재고 탭 내용
with tab1:
    st.header("전체 재고")
    st.write("여기에 전체 재고 리스트를 표시합니다.")

# 보유함 탭 내용
with tab2:
    st.header("보유함")
    st.write("현재 보유 중인 재고를 표시합니다.")

# 구매 예정 탭 내용
with tab3:
    st.header("구매 예정")
    st.write("구매 예정인 항목들을 표시합니다.")

# 배송 중 탭 내용
with tab4:
    st.header("배송 중")
    st.write("배송 중인 항목들을 표시합니다.")

# 초기 데이터프레임 설정
initial_data = pd.DataFrame(
    [
        {"부품명": "", "개수(개)": 0, "보유함": False, "구매 예정": False, "배송 중": False}
    ]
)

# 세션 상태에 초기화된 데이터가 없으면 기본값 설정
if 'data' not in st.session_state:
    st.session_state.data = initial_data

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

# 개수(개)를 기본 1로 설정
개수 = st.number_input("개수(개)", min_value=1, value=1, key='개수(개)')

# "보유함", "구매 예정", "배송 중" 중 하나만 선택할 수 있게 라디오 버튼 사용
상태 = st.radio("상태 선택", ('보유함', '구매 예정', '배송 중'), key='상태')

# 각 상태에 맞는 체크박스 값을 결정
보유함 = 상태 == '보유함'
구매예정 = 상태 == '구매 예정'
배송중 = 상태 == '배송 중'

if st.button("부품 추가"):
    # 비어있는 행 찾기
    empty_row_index = st.session_state.data[st.session_state.data['부품명'] == ""].index

    if not empty_row_index.empty:
        # 비어있는 첫 번째 행에 추가
        first_empty_index = empty_row_index[0]
        st.session_state.data.at[first_empty_index, '부품명'] = 부품명
        st.session_state.data.at[first_empty_index, '개수(개)'] = 개수
        st.session_state.data.at[first_empty_index, '보유함'] = 보유함
        st.session_state.data.at[first_empty_index, '구매 예정'] = 구매예정
        st.session_state.data.at[first_empty_index, '배송 중'] = 배송중
    else:
        # 비어있는 행이 없으면 새로운 행 추가
        new_row = pd.DataFrame({
            "부품명": [부품명], 
            "개수(개)": [개수], 
            "보유함": [보유함], 
            "구매 예정": [구매예정], 
            "배송 중": [배송중]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

    st.success("부품이 추가되었습니다!")
else:
    st.warning("부품명과 개수를 확인하세요.")

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

# 사이드바에 여러 가지 위젯을 추가
sidebar = st.sidebar

# 사이드바에 버튼으로 "전체 재고" 추가
if st.sidebar.button('전체 재고'):
    st.sidebar.write("전체 재고를 클릭했습니다!")

st.sidebar.markdown("  - **보유함**")
st.sidebar.markdown("  - **구매 예정**")
st.sidebar.markdown("  - **배송 중**")


# 사이드바에 재고 수정 타이틀 추가
st.sidebar.title('재고 수정')

st.sidebar.text('데이터 공유')


# 사이드바에 텍스트 링크처럼 보이는 클릭 가능한 항목 추가
if st.sidebar.markdown('[전체 재고](#)', unsafe_allow_html=True):
    st.sidebar.write("전체 재고를 클릭했습니다!")