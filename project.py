import streamlit as st
import pandas as pd

st.title("📦재고관리 앱📦")

# CSV 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일 업로드", type='csv')

# 사이드바에 버튼 추가
st.sidebar.title("📦재고관리 앱📦")
page = st.sidebar.radio("", ("재고 데이터베이스", "재고 수정"))

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

# 데이터 병합 함수: 같은 부품명과 상태가 같으면 개수를 합침
def merge_duplicate_entries(df):
    merged_df = df.groupby(['부품명', '보유함', '구매 예정', '배송 중'], as_index=False).agg({'개수(개)': 'sum'})
    merged_df['개수(개)'] = merged_df['개수(개)'].astype(int)
    merged_df = merged_df[['부품명', '개수(개)', '보유함', '구매 예정', '배송 중']]
    return merged_df

# 상태가 한 번에 하나만 True가 될 수 있도록 강제하는 함수
def ensure_single_true_state(df):
    for i in df.index:
        true_columns = ['보유함', '구매 예정', '배송 중']
        true_count = df.loc[i, true_columns].sum()
        if true_count > 1:  # 여러 개가 True일 때
            first_true = df.loc[i, true_columns].idxmax()  # 첫 번째 True 값만 유지
            for col in true_columns:
                df.at[i, col] = (col == first_true)  # 첫 번째 True 외에 나머지는 False로 설정
        elif true_count == 0:  # 모두 False일 때는 기본값으로 '보유함'을 True로 설정
            df.at[i, '보유함'] = True
    return df

# 페이지에 따른 콘텐츠 출력
if page == "재고 데이터베이스":
    st.header("재고 데이터베이스")
    
    # 데이터를 병합하여 중복된 부품을 합침
    merged_data = merge_duplicate_entries(st.session_state.data)
    
    # 병합된 데이터를 세션 상태에 저장 (재고 수정에서 사용할 수 있도록)
    st.session_state.merged_data = merged_data

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
        
        # 데이터 에디터에서 수정된 내용을 가져옴
        edited_df = st.data_editor(st.session_state.merged_data)

        # 상태를 하나만 True로 강제
        edited_df = ensure_single_true_state(edited_df)

        # 수정된 내용을 세션 상태에 반영
        st.session_state.data = edited_df
        st.session_state.merged_data = edited_df

# 사용자로부터 파일명 입력받기
file_name = st.text_input("저장할 파일명", "재고리스트.csv")

# 수정된 데이터프레임을 CSV로 다운로드
if st.button("다운로드"):
    csv = st.session_state.merged_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSV 다운로드",
        data=csv,
        file_name=file_name,
        mime='text/csv',
    )
