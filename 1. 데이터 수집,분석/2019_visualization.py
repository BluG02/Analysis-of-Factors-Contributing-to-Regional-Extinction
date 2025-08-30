import pandas as pd, geopandas as gpd, folium, numpy as np

# ────────────────────────────────
# 데이터 로드
risk_df = pd.read_csv("인구소멸지수19.csv", encoding="utf-8-sig")
geo = gpd.read_file("TL_SCCO_SIG.json", encoding="utf-8")

# 병합
merged = geo.merge(risk_df, left_on="SIG_KOR_NM", right_on="도시", how="left")

vals = merged["인구소멸지수"].dropna()
vmin, vmax = vals.min(), vals.max()

# *구간 4개* 예시: min → 0.5 → 0.8 → 1.1 → max
bins = [vmin,
        0.5 if 0.5 > vmin else vmin + 0.0001,   # 겹치지 않도록 +ε
        0.8 if 0.8 < vmax else vmax - 0.0001,
        1.1 if 1.1 < vmax else vmax - 0.0001,
        vmax + 0.0001]                           # 맨 끝은 max 초과

print("★ bins:", bins)  # 확인용

# ────────────────────────────────
# 지도
m = folium.Map(location=[36.5, 127.9], zoom_start=7, tiles="cartodbpositron")

folium.Choropleth(
    geo_data=merged,
    data=merged,
    columns=["SIG_KOR_NM", "인구소멸지수"],
    key_on="feature.properties.SIG_KOR_NM",
    bins=bins,                  # ← 자동 bins 사용
    fill_color="RdYlGn",
    line_opacity=0.5,
    legend_name="인구소멸지수",
    nan_fill_color="lightgrey"
).add_to(m)

m.save("Korea_Risk_Choropleth_fixed.html")
print("✅ Choropleth 생성 완료!")