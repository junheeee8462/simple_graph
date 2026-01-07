import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("그래프 툴")

# 1. 입력부
col1, col2 = st.columns(2)
with col1:
    x_input = st.text_input("X축 숫자 (쉼표 구분)", "10,20,30,40,50,60")
with col2:
    y_input = st.text_input("Y축 숫자 (쉼표 구분)", "12,23,36,41,58,61")

try:
    # 문자열 -> 숫자 리스트 변환
    x_list = np.array([float(x.strip()) for x in x_input.split(",") if x.strip()])
    y_list = np.array([float(y.strip()) for y in y_input.split(",") if y.strip()])

    if len(x_list) == len(y_list) and len(x_list) > 1:
        
        # --- 2. 계산부 ---
        
        # A. 평균 Gain 계산 (y/x의 평균)
        gains = [y / x for x, y in zip(x_list, y_list) if x != 0]
        avg_gain = sum(gains) / len(gains)
        y_avg_gain = avg_gain * x_list  # 평균 Gain을 적용한 Y 값들

        # B. 선형 회귀 (Linear Regression) 계산
        # 1차식(y = ax + b)으로 피팅
        slope, intercept = np.polyfit(x_list, y_list, 1)
        y_regression = slope * x_list + intercept # 회귀선 Y 값들

        # --- 3. 그래프 그리기 (Matplotlib) ---
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 원본 데이터 (점과 점선)
        ax.plot(x_list, y_list, 'o-', label='Original Data', color='#1f77b4', markersize=8)
        
        # 평균 Gain 선 (원점을 지나는 직선)
        ax.plot(x_list, y_avg_gain, '--', label=f'Avg Gain Line (Gain: {avg_gain:.2f})', color='#ff7f0e')
        
        # 선형 회귀선 (최적 적합선)
        ax.plot(x_list, y_regression, '-', label=f'Regression Line (Slope: {slope:.2f})', color='#2ca02c', linewidth=2)

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_title('Data Analysis: Average Gain vs Linear Regression')
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

        # 스트림릿에 출력
        st.pyplot(fig)

        # --- 4. 지표 표시 (Metrics) ---
        st.divider()
        m1, m2 = st.columns(2)
        m1.metric("선형 회귀 기울기 (Slope)", f"{slope:.2f}")
        m2.metric("평균 Gain", f"{avg_gain:.2f}")
        
        if intercept != 0:
            st.caption(f"회귀식: y = {slope:.2f}x + {intercept:.2f}")

    elif len(x_list) != len(y_list):
        st.warning("X축과 Y축의 데이터 개수가 일치하지 않습니다.")
    else:
        st.info("데이터를 입력해 주세요.")

except ValueError:
    st.error("숫자 형식이 올바르지 않습니다. 쉼표로 구분된 숫자만 입력해주세요.")

st.divider()
st.subheader("📚 결과 해석 가이드")

with st.expander("1. 평균 Gain과 선형 회귀 Gain의 차이는 무엇인가요?"):
    st.markdown("""
    * **평균 Gain ($Y/X$의 평균):** * 각 데이터 지점에서의 '효율'이나 '비율'을 각각 구한 뒤 산술 평균을 낸 값입니다.
        * **의미:** "개별 측정값들이 평균적으로 몇 배의 출력을 내는가?"를 나타냅니다.
        * **특징:** 원점(0,0)에서 시작하는 비례 관계를 가정할 때 유용하지만, 측정값에 0에 가까운 값이 있거나 편차가 크면 왜곡될 수 있습니다.

    * **선형 회귀 Gain (기울기, Slope):** * 모든 데이터 점들과의 거리가 최소가 되는 '최적의 직선'을 구했을 때의 기울기입니다.
        * **의미:** "입력($X$)이 1단위 증가할 때 출력($Y$)이 **전체적으로 얼마나 변하는가**"라는 **추세(Trend)**를 나타냅니다.
        * **특징:** 데이터에 상수적인 오차(y절편)가 있더라도 전체적인 변화율을 정확하게 포착합니다.
    """)

with st.expander("2. 그래프를 어떻게 해석해야 하나요?"):
    st.markdown("""
    * **데이터 점들이 직선 위에 몰려 있는 경우:** 시스템이 매우 안정적이고 예측 가능함을 의미합니다.
    * **두 선(주황색 vs 초록색)이 비슷할 경우:** 데이터가 원점을 지나는 정비례 관계에 가깝다는 뜻입니다.
    * **두 선의 간격이 넓은 경우:** 데이터에 일정한 기본값(Offset)이 존재하거나, 특정 구간에서 Gain이 급격히 변하고 있음을 시사합니다.
    * **원본 데이터(파란색)가 요동치는 경우:** 외부 노이즈가 많거나 측정 환경이 불안정할 수 있습니다.
    """)


