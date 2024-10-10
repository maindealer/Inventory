import streamlit as st
import pandas as pd
import io

st.title("📦재고관리 앱📦")

# 사이드바에 버튼 추가
st.sidebar.title("📦재고관리 앱📦")
page = st.sidebar.radio("", ("📊 재고 데이터베이스", "🛠 재고 수정"))

# 초기 데이터프레임 설정
initial_data = pd.DataFrame(
    [
        {"부품명": "", "개수(개)": 0, "보유함": False, "구매 예정": False, "배송 중": False, "구매일자": ""}
    ]
)

# 세션 상태에 초기화된 데이터가 없으면 기본값 설정
if 'data' not in st.session_state:
    st.session_state.data = initial_data

# 페이지에 따른 콘텐츠 출력
if page == "📊 재고 데이터베이스":
    st.header("📊 재고 데이터베이스")
    
    # CSV 파일 업로드 기능을 이곳에 추가
    uploaded_file = st.file_uploader("📁 CSV 파일 업로드", type='csv')

    # 파일이 업로드되었을 때 세션 상태에 데이터 업데이트
    if uploaded_file is not None:
        st.session_state.data = pd.read_csv(uploaded_file)
        st.session_state['uploaded'] = True
    elif uploaded_file is None and 'uploaded' not in st.session_state:
        # 파일이 없을 때는 초기 데이터로 복원
        st.session_state.data = initial_data

    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["🗃 전체 재고", "✅ 보유함", "🛒 구매 예정", "📦 배송 중"])

    # 각 탭별 재고 데이터 표시
    with tab1:
        st.subheader("🗃 전체 재고")
        st.dataframe(st.session_state.data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    with tab2:
        st.subheader("✅ 보유함")
        stock_data = st.session_state.data[st.session_state.data['보유함']]
        st.dataframe(stock_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    with tab3:
        st.subheader("🛒 구매 예정")
        purchase_data = st.session_state.data[st.session_state.data['구매 예정']]
        st.dataframe(purchase_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    with tab4:
        st.subheader("📦 배송 중")
        delivery_data = st.session_state.data[st.session_state.data['배송 중']]
        st.dataframe(delivery_data.style.set_properties(subset=['부품명'], **{'width': '300px'}))

    # 부품명 검색 입력창 추가
    search_part = st.text_input("🔍 부품명 검색", "")

    # 검색한 부품명으로 데이터 필터링
    if search_part:
        # 대소문자를 구분하지 않고, 부품명이 완전히 일치하는 행을 검색
        search_results = st.session_state.data[
            st.session_state.data['부품명'].str.lower() == search_part.lower()
        ]
        
        if not search_results.empty:
            # 검색한 부품명 결과를 데이터프레임으로 표시
            st.write(f"**'{search_part}' 부품의 검색 결과**")
            st.dataframe(search_results.style.set_properties(subset=['부품명'], **{'width': '300px'}))
            
            # 상태별 개수 계산
            in_stock_count = search_results[search_results['보유함']]['개수(개)'].sum() if not search_results[search_results['보유함']].empty else 0
            purchase_count = search_results[search_results['구매 예정']]['개수(개)'].sum() if not search_results[search_results['구매 예정']].empty else 0
            delivery_count = search_results[search_results['배송 중']]['개수(개)'].sum() if not search_results[search_results['배송 중']].empty else 0
            
            # 각 상태별로 출력
            st.write(f"**'{search_part}' 부품의 상태별 개수**")
            st.write(f"🔹 **보유 중**: {in_stock_count}개")
            st.write(f"🔹 **구매 예정**: {purchase_count}개")
            st.write(f"🔹 **배송 중**: {delivery_count}개")
            
        else:
            st.write(f"**'{search_part}' 부품을 찾을 수 없습니다.**")

elif page == "🛠 재고 수정":
    # CSV 파일이 업로드된 경우에만 재고 수정 페이지 표시
    if 'uploaded' in st.session_state and st.session_state['uploaded']:
        st.header("🛠 재고 수정")
        
        # 업로드된 데이터를 재고 수정 페이지에서 사용
        if 'data' in st.session_state:
            
            # 세션 상태에 임시 데이터를 저장
            if 'temp_data' not in st.session_state:
                st.session_state.temp_data = st.session_state.data.copy()
            
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
            
            # 저장 버튼
            if st.button("✅ 저장"):
                st.session_state.data = st.session_state.temp_data.copy()
                st.success("변경 사항이 저장되었습니다.")
            
            # 업데이트된 데이터 출력
            st.subheader("수정된 데이터")
            st.dataframe(st.session_state.temp_data)

            # CSV 파일 이름 입력
            file_name = st.text_input("📁 저장할 파일 이름을 입력하세요.")
            
            # CSV 다운로드 버튼 추가
            if st.button("💾 수정된 데이터 CSV로 저장"):
                # 파일명으로 수정된 데이터를 저장
                csv = st.session_state.temp_data.to_csv(index=False)
                st.download_button(
                    label="다운로드",
                    data=csv,
                    file_name=f"{file_name}",
                    mime="text/csv"
                )
    else:
        st.warning("재고 수정 페이지에 들어가기 위해서는, 먼저 CSV 파일을 업로드해야 합니다.")