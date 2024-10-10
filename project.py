import streamlit as st
import pandas as pd

st.title("📦재고관리 앱📦")

# 사이드바에 버튼 추가
st.sidebar.title("📦재고관리 앱📦")
page = st.sidebar.radio("", ("재고 데이터베이스", "재고 수정"))

# 초기 데이터프레임 설정
initial_data = pd.DataFrame(
    [
        {"부품명": "", "개수(개)": 0, "보유함": False, "구매 예정": False, "배송 중": False, "구매일자": ""}
    ]
)

# 세션 상태에 초기화된 데이터가 없으면 기본값 설정
if 'data' not in st.session_state:
    st.session_state.data = initial_data

# 데이터 병합 함수: 같은 부품명과 상태가 같으면 개수를 합침
def merge_duplicate_entries(df):
    merged_df = df.groupby(['부품명', '보유함', '구매 예정', '배송 중', '구매일자'], as_index=False).agg({'개수(개)': 'sum'})
    merged_df = merged_df[['부품명', '개수(개)', '보유함', '구매 예정', '배송 중', '구매일자']]
    return merged_df

# 페이지에 따른 콘텐츠 출력
if page == "재고 데이터베이스":
    st.header("재고 데이터베이스")
    
    # CSV 파일 업로드 기능을 이곳에 추가
    uploaded_file = st.file_uploader("CSV 파일 업로드", type='csv')

    # 파일이 업로드되었을 때 세션 상태에 데이터 업데이트
    if uploaded_file is not None:
        st.session_state.data = pd.read_csv(uploaded_file)
        st.session_state['uploaded'] = True
    elif uploaded_file is None and 'uploaded' not in st.session_state:
        # 파일이 없을 때는 초기 데이터로 복원
        st.session_state.data = initial_data

    # 데이터를 병합하여 중복된 부품을 합침
    merged_data = merge_duplicate_entries(st.session_state.data)
    st.session_state.merged_data = merged_data  # 병합된 데이터를 세션 상태에 저장

    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["전체 재고", "보유함", "구매 예정", "배송 중"])
    
    # 전체 재고 탭 내용
    with tab1:
        st.subheader("전체 재고")
        st.dataframe(merged_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    # 보유함 탭 내용
    with tab2:
        st.subheader("보유함")
        stock_data = merged_data[merged_data['보유함']]
        st.dataframe(stock_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    # 구매 예정 탭 내용
    with tab3:
        st.subheader("구매 예정")
        purchase_data = merged_data[merged_data['구매 예정']]
        st.dataframe(purchase_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    # 배송 중 탭 내용
    with tab4:
        st.subheader("배송 중")
        delivery_data = merged_data[merged_data['배송 중']]
        st.dataframe(delivery_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

elif page == "재고 수정":
    st.header("재고 수정")
    
    # 병합된 데이터를 재고 수정 페이지에서 사용
    if 'merged_data' in st.session_state:
        st.subheader("수정 가능한 재고 리스트")
        
        # 세션 상태에 임시 데이터를 저장
        if 'temp_data' not in st.session_state:
            st.session_state.temp_data = st.session_state.merged_data.copy()
        
        # 수정 가능한 테이블을 위해 각 열에 대한 동작 제어
        def enforce_unique_selection(row):
            """
            보유함, 구매 예정, 배송 중 중 하나만 True가 되도록 하는 함수.
            """
            # 하나의 열만 True로 설정
            if row['보유함']:
                row['구매 예정'] = False
                row['배송 중'] = False
            elif row['구매 예정']:
                row['보유함'] = False
                row['배송 중'] = False
            elif row['배송 중']:
                row['보유함'] = False
                row['구매 예정'] = False
            return row

        # 수정된 데이터는 세션 상태의 임시 데이터에 저장
        edited_data = st.data_editor(
            st.session_state.temp_data,
            num_rows="dynamic",
            key="editable_inventory"
        )
        
        # 유일 선택 강제 적용
        st.session_state.temp_data = edited_data.apply(enforce_unique_selection, axis=1)
        
        # 저장 버튼 추가
        if st.button("저장"):
            st.session_state.merged_data = st.session_state.temp_data.copy()
            st.success("변경 사항이 저장되었습니다.")
        
        # 업데이트된 데이터 출력
        st.subheader("수정된 데이터")
        st.dataframe(st.session_state.temp_data)
