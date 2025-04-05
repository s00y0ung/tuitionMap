import pandas as pd
import folium

df = pd.read_excel('registration.xlsx')
df.drop([0], axis = 0, inplace = True)
# TuitionAnalysis.py 내용
df = df.drop(df[df['상태'] == '폐교'].index, axis = 0)
df = df.rename(columns = {'등록금\n(D=B)':'등록금', '수업료\n(B)':'수업료'})
df = df.drop(df[df['등록금'] == 0.0].index, axis = 0)

df = df[['학교종류','설립구분','지역','학교','수업료','등록금']]
df = df.replace({'설립구분':'공립'},'국립')
df = df.replace({'설립구분':'국립대법인'}, '국립')
df = df.replace({'설립구분':'특별법법인'},'특별')
df = df.replace({'설립구분':'특별법국립'},'특별')

# 대학원 소재지가 도로명주소로 되어있는 자료
univ_df = pd.read_csv('university.csv', encoding = 'cp949')

# 대학구분 확인 코드 univ_df['대학구분명'].value_counts()
# 대학원 1520, 대학 261, 전문대학 180 --> 대학원 없애버리기
univ_df = univ_df[univ_df['대학구분명'] != '대학원']

# 필요한 데이터(row)만 추출하기
# 학교명, 설립형태구분명, 소재지도로명주소
univ_df = univ_df[['학교명','설립형태구분명', '소재지도로명주소']]

# 데이터 전처리
# 1. 학교명에 대학원 붙이지 않기..
univ_name = univ_df['학교명'].str.split().str[0]
univ_df.loc[:, '학교명'] = univ_name

# 2. 중복되는 학교명 없애버리기 (대학원을 없애버리면서 ex. 경북대학교 대학원, 경북대학교가 동일시되어버림.)
univ_df.drop_duplicates(subset = '학교명', ignore_index = True, inplace = True)


# univ_df, df를 합치기 (inner join)
u_df = pd.merge(univ_df, df, left_on = '학교명', right_on = '학교')
# 겹치는 행렬은 없애기
u_df = u_df.drop(labels = '학교', axis = 1)
u_df = u_df.drop(labels = '설립구분', axis = 1)

# 소재지 도로명 주소를 구 > 군 > 시 까지 나타내기
u_df['세부지역'] = u_df['소재지도로명주소'].str.split(' ').str[1]
u_df['세부지역2'] = u_df['소재지도로명주소'].str.split(' ').str[2]
u_df.loc[u_df['세부지역2'].str.endswith('구'), '세부지역'] = u_df['세부지역'] + u_df['세부지역2']

# 지도 =====================================
geo_json_url = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json'
# 지도 생성
m = folium.Map(location=[36, 127], zoom_start=7)
# Choropleth 추가
folium.Choropleth(
    geo_data=geo_json_url,
    data=u_df,
    columns=['세부지역', '등록금'],
    key_on='feature.properties.name', # GeoJSON의 지역명 속성
    fill_color='BuPu',
    fill_opacity=0.7, #색 투명도
    line_opacity=0.5, #선 투명도
    legend_name='등록금'
).add_to(m)

# 지도 저장
m.save('choropleth_tution_total.html')