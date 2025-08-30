import pandas as pd

# 반복 처리할 연도 (두 자리)
years = range(18, 24)  # 2018 ~ 2023

for year in years:
    try:
        file_path = f"인구소멸지수{year}.csv"
        df = pd.read_csv(file_path, encoding="utf-8-sig")

        # 필요한 컬럼만 추출
        df = df[['도시', '인구소멸지수']].copy()

        # 숫자형 변환 및 결측치 제거
        df['인구소멸지수'] = pd.to_numeric(df['인구소멸지수'], errors='coerce')
        df = df.dropna(subset=['인구소멸지수'])

        # 상위 10개
        top10 = (
            df.sort_values('인구소멸지수', ascending=False)
              .head(10)
              .assign(구분='상위')
        )

        # 하위 10개
        bottom10 = (
            df.sort_values('인구소멸지수', ascending=True)
              .head(10)
              .assign(구분='하위')
        )

        # 합치고 소수점 반올림
        combined = (
            pd.concat([top10, bottom10])
              .reset_index(drop=True)
              .round({'인구소멸지수': 2})
        )

        # 저장
        output_path = f"인구소멸지수{year}_top_bottom10.csv"
        combined.to_csv(output_path, index=False, encoding="utf-8-sig")

        print(f"✅ 20{year}년 결과 저장 완료 → {output_path}")
        print(combined, "\n")

    except Exception as e:
        print(f"⚠️ 20{year}년 처리 중 오류 발생: {e}\n")