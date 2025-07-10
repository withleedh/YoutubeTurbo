import streamlit as st
import streamlit.components.v1 as components
import os
import base64

def get_webfont_css(font_filename):
    """한글 웹폰트 CDN CSS 생성"""
    webfont_mapping = {
        # 나눔스퀘어 시리즈 (moonspam CDN)
        'NanumSquareR.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css");',
            'family': 'NanumSquare',
            'weight': '400'
        },
        'NanumSquareB.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css");',
            'family': 'NanumSquare', 
            'weight': '700'
        },
        'NanumSquareEB.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css");',
            'family': 'NanumSquare',
            'weight': '800'
        },
        'NanumSquareL.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css");',
            'family': 'NanumSquare',
            'weight': '300'
        },
        
        # 나눔스퀘어 네오 시리즈 (eunchurn CDN)
        'NanumSquareNeoLight.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/eunchurn/NanumSquareNeo@0.0.6/nanumsquareneo.css");',
            'family': 'NanumSquareNeo',
            'weight': '100'
        },
        'NanumSquareNeoRegular.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/eunchurn/NanumSquareNeo@0.0.6/nanumsquareneo.css");',
            'family': 'NanumSquareNeo',
            'weight': '300'
        },
        'NanumSquareNeoBold.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/eunchurn/NanumSquareNeo@0.0.6/nanumsquareneo.css");',
            'family': 'NanumSquareNeo',
            'weight': '500'
        },
        'NanumSquareNeoExtraBold.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/eunchurn/NanumSquareNeo@0.0.6/nanumsquareneo.css");',
            'family': 'NanumSquareNeo',
            'weight': '700'
        },
        'NanumSquareNeoHeavy.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/eunchurn/NanumSquareNeo@0.0.6/nanumsquareneo.css");',
            'family': 'NanumSquareNeo',
            'weight': '800'
        },
        
        # 나눔바른고딕 (moonspam CDN)
        'NanumBarunGothic.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumBarunGothic@latest/nanumbarungothicsubset.css");',
            'family': 'NanumBarunGothic',
            'weight': '400'
        },
        'NanumBarunGothicBold.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumBarunGothic@latest/nanumbarungothicsubset.css");',
            'family': 'NanumBarunGothic',
            'weight': '700'
        },
        'NanumBarunGothicLight.ttf': {
            'css': '@import url("https://cdn.jsdelivr.net/gh/moonspam/NanumBarunGothic@latest/nanumbarungothicsubset.css");',
            'family': 'NanumBarunGothic',
            'weight': '300'
        },
    }
    
    return webfont_mapping.get(font_filename)

def get_font_display_name(font_filename):
    """폰트 파일명을 보기 좋은 이름으로 변환"""
    name_mapping = {
        # 나눔스퀘어 네오
        'NanumSquareNeoLight.ttf': '나눔스퀘어 네오 Light',
        'NanumSquareNeoRegular.ttf': '나눔스퀘어 네오 Regular', 
        'NanumSquareNeoBold.ttf': '나눔스퀘어 네오 Bold',
        'NanumSquareNeoExtraBold.ttf': '나눔스퀘어 네오 ExtraBold',
        'NanumSquareNeoHeavy.ttf': '나눔스퀘어 네오 Heavy',
        
        # 나눔바른고딕
        'NanumBarunGothic.ttf': '나눔바른고딕 Regular',
        'NanumBarunGothicBold.ttf': '나눔바른고딕 Bold',
        'NanumBarunGothicLight.ttf': '나눔바른고딕 Light',
        
        # 나눔스퀘어
        'NanumSquareR.ttf': '나눔스퀘어 Regular',
        'NanumSquareB.ttf': '나눔스퀘어 Bold',
        'NanumSquareEB.ttf': '나눔스퀘어 ExtraBold',
        'NanumSquareL.ttf': '나눔스퀘어 Light',
        
        # 기타
        'BMDOHYEON.ttf': '배달의민족 도현체',
        
        # Pretendard
        'Pretendard-Regular.ttf': 'Pretendard Regular',
        'Pretendard-Bold.ttf': 'Pretendard Bold',
        'Pretendard-Medium.ttf': 'Pretendard Medium',
        'Pretendard-Light.ttf': 'Pretendard Light',
    }
    
    return name_mapping.get(font_filename, font_filename.replace('.ttf', '').replace('.ttc', ''))

def font_selector_with_preview(label, font_names, font_dir, selected_index=0, preview_text="가나다ABC123", tr_func=None):
    """폰트 선택기와 실제 폰트 미리보기 컴포넌트"""
    if tr_func is None:
        tr_func = lambda x: x
    
    # 보기 좋은 폰트 이름으로 표시
    display_options = [get_font_display_name(font) for font in font_names]
    
    # selectbox를 보기 좋은 이름으로 표시
    selected_display_name = st.selectbox(
        label, 
        display_options, 
        index=selected_index,
        key="font_selector"
    )
    
    # 실제 파일명 찾기
    selected_font = font_names[display_options.index(selected_display_name)]
    
    # 선택된 폰트의 미리보기 생성
    if selected_font:
        font_path = os.path.join(font_dir, selected_font)
        
        if os.path.exists(font_path):
            # CDN 웹폰트 확인
            webfont_info = get_webfont_css(selected_font)
            
            # 실제 CDN 웹폰트로 미리보기
            if webfont_info:
                preview_html = f"""
                <style>
                {webfont_info['css']}
                .font-preview {{
                    font-family: '{webfont_info['family']}', sans-serif;
                    font-size: 32px;
                    color: #212529;
                    font-weight: {webfont_info['weight']};
                    margin: 8px 0;
                    padding: 16px;
                    background: white;
                    border-radius: 8px;
                    border: 2px solid #28a745;
                    letter-spacing: 1px;
                    text-align: center;
                }}
                </style>
                <div style="
                    padding: 15px;
                    border: 2px solid #28a745;
                    border-radius: 8px;
                    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                    margin: 10px 0;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(40,167,69,0.2);
                ">
                    <div style="
                        font-size: 14px;
                        color: #155724;
                        margin-bottom: 8px;
                        font-weight: 600;
                    ">
                        ✨ 실제 폰트 미리보기: <strong>{selected_display_name}</strong>
                    </div>
                    <div class="font-preview">
                        {preview_text}
                    </div>
                    <div style="
                        font-size: 12px;
                        color: #155724;
                        margin-top: 8px;
                        font-weight: 500;
                    ">
                        ✅ CDN 웹폰트 ({webfont_info['family']}, Weight: {webfont_info['weight']}) | 최적화된 WOFF2 로드
                    </div>
                </div>
                """
            else:
                # 큰 폰트는 이름만 표시
                preview_html = f"""
                <div style="
                    padding: 15px;
                    border: 2px solid #ffc107;
                    border-radius: 8px;
                    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                    margin: 10px 0;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(255,193,7,0.2);
                ">
                    <div style="
                        font-size: 14px;
                        color: #856404;
                        margin-bottom: 8px;
                        font-weight: 500;
                    ">
                        📝 선택된 폰트: <strong>{selected_display_name}</strong>
                    </div>
                    <div style="
                        font-size: 28px;
                        color: #212529;
                        font-weight: bold;
                        margin: 8px 0;
                        padding: 12px;
                        background: white;
                        border-radius: 5px;
                        border: 1px solid #dee2e6;
                        letter-spacing: 1px;
                        font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
                    ">
                        {preview_text}
                    </div>
                    <div style="
                        font-size: 12px;
                        color: #856404;
                        margin-top: 8px;
                    ">
                        ⚡ 파일 크기가 커서 미리보기는 기본 폰트로 표시됩니다<br>
                        💡 실제 자막에는 선택한 폰트가 정확히 적용됩니다
                    </div>
                </div>
                """
            
            components.html(preview_html, height=180)
            
            # 폰트 정보 표시
            file_size = os.path.getsize(font_path) / (1024 * 1024)  # MB
            with st.expander(f"📋 {selected_display_name} 정보"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**파일명**: `{selected_font}`")
                    st.markdown(f"**크기**: `{file_size:.1f} MB`")
                with col2:
                    st.markdown(f"**타입**: `{'CDN 웹폰트 미리보기' if webfont_info else '파일명 미리보기'}`")
                    st.markdown(f"**상태**: `{'✅ 사용 가능' if os.path.exists(font_path) else '❌ 파일 없음'}`")
                
                st.markdown("---")
                st.markdown("**🎭 사용 가능한 한글 폰트 모음**:")
                st.markdown("""
                - **나눔스퀘어 네오** (최신, 깔끔한 디자인)
                - **나눔바른고딕** (읽기 좋은 고딕체)
                - **나눔스퀘어** (각진 디자인)
                - **Pretendard** (범용성 좋은 현대적 폰트)
                - **배달의민족 도현체** (개성 있는 디자인)
                """)
                
        else:
            st.error(f"⚠️ 폰트 파일을 찾을 수 없습니다: {font_path}")
    
    return selected_font 