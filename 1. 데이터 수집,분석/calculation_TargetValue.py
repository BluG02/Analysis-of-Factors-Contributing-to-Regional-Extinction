import pandas as pd
import numpy as np

# 연도 반복 (두 자리)
years = range(18, 24)

for year in years:
    try:
        file_path = f"인구{year}.xlsx"
        xls = pd.ExcelFile(file_path)
        df = xls.parse('데이터')

        df['시점'] = df['시점'].ffill()
        df['행정구역(시군구)별'] = df['행정구역(시군구)별'].ffill()

        young_female_cols = ['20 - 24세', '25 - 29세', '30 - 34세', '35 - 39세']
        elder_cols = ['65 - 69세', '70 - 74세', '75 - 79세', '80세 이상']

        aggregated_data = {}

        for _, row in df.iterrows():
            if pd.isna(row['시점']) or pd.isna(row['행정구역(시군구)별']):
                continue

            current_year = int(row['시점'])
            current_city = str(row['행정구역(시군구)별']).strip()
            key = (current_year, current_city)

            if key not in aggregated_data:
                aggregated_data[key] = {
                    '연도': current_year,
                    '도시': current_city,
                    '20-39세 여성': 0,
                    '65세 이상 인구': 0
                }

            if row['성별'] == '여자':
                young_female_count = sum([
                    row[col] for col in young_female_cols
                    if pd.notna(row[col]) and row[col] != '-'
                ])
                aggregated_data[key]['20-39세 여성'] += young_female_count

                elder_female_count = sum([
                    row[col] for col in elder_cols
                    if pd.notna(row[col]) and row[col] != '-'
                ])
                aggregated_data[key]['65세 이상 인구'] += elder_female_count

            elif row['성별'] == '남자':
                elder_male_count = sum([
                    row[col] for col in elder_cols
                    if pd.notna(row[col]) and row[col] != '-'
                ])
                aggregated_data[key]['65세 이상 인구'] += elder_male_count

        rows = []
        for data_values in aggregated_data.values():
            young_female_total = data_values['20-39세 여성']
            total_elder = data_values['65세 이상 인구']
            index = None
            if total_elder > 0:
                index = young_female_total / total_elder
            elif young_female_total > 0 and total_elder == 0:
                index = np.inf
            rows.append({
                '연도': data_values['연도'],
                '도시': data_values['도시'],
                '인구소멸지수': index
            })

        extinction_index_df = pd.DataFrame(rows)
        output_path = f"인구소멸지수{year}.csv"
        extinction_index_df.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"✅ 20{year}년 처리 완료 → {output_path}")
        print(f"→ 도시 수: {extinction_index_df['도시'].nunique()}개\n")

    except Exception as e:
        print(f"⚠️ 20{year}년 처리 중 오류 발생: {e}")