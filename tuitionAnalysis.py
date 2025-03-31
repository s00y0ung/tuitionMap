import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('registration.xlsx')

#첫번째 행 삭제
df.drop([0], axis = 0, inplace = True)

# 학교 종류 확인하기
#print(df['학교종류'].value_counts())
# 대학교 209, 사이버대학 17, 교육 대학 10, ,, 확인가능

## 데이터 전처리 시작
# 1. 상태가 폐교인 학교는 삭제
# 2. 등록금, 수업료로 열 이름 바꾸기
# 3. 등록금 == 0인 학교는 삭제
# 4. 학교 종류, 설립 구분, 지역, 학교, 수업료, 등록금 row 사용
#=====================================================

# 1. 상태가 폐교인 학교는 삭제
df = df.drop(df[df['상태'] == "페교"].index, axis = 0)
# 2. 등록금, 수업료 (열 이름 바꾸기)
df = df.rename(columns = {'등록금\n(D=B)':'등록금', '수업료\n(B)':'수업료'})
# 3. 등록금 == 0인 학교는 삭제
df = df.drop(df[df['등록금'] == 0.0].index, axis = 0)
# 4. 필요한 row만 가져오기
df = df[['학교종류','설립구분','지역','학교','수업료','등록금']]
print(df.columns)

## 데이터 시각화 시작
plt.rcParams['font.family'] = 'Malgun Gothic'
## 지역별 등록금 평균 barplot
# sns.set_theme(rc = {'figure.figsize' : (10,6)}, style = 'white')
# sns.barplot(data = df, x ="지역", y = "등록금", errorbar = None)
# plt.ylabel('등록금(백만)')
# plt.title('지역별 등록금 현황')
#plt.show()

## 지역별로 학교 몇 개가 존재하는지 알아보기 histplot
# sns.histplot(data = df, x = "지역", color = '#F4A0A0')
# plt.title("지역별 학교 개수")
#df['지역'].value_counts()로 상세확률 확인가능
#plt.show()

## 국립 사립으로 등록금 비교 barplot
# sns.barplot(data = df, x = "설립구분", y = "등록금", errorbar = None)
# plt.title("설립 구분 별 등록금 비교")
# plt.ylabel("등록금(백만)")
# plt.show()

#공립과 국립대 법인을 국립으로
#특별법법인과 특별법국립을 특별로 한 곳으로 묶기
df = df.replace({'설립구분':'공립'},'국립')
df = df.replace({'설립구분':'국립대법인'}, '국립')
df = df.replace({'설립구분':'특별법법인'},'특별')
df = df.replace({'설립구분':'특별법국립'},'특별')
#df['설립구분'].value_counts()

## 지역별 국립, 사립 등록금 현황 확인
# sns.barplot(data = df, x = "지역", y = "등록금", hue = "설립구분", errorbar = None)
# plt.ylabel("등록금(백만)")
# plt.show()

## 수업료, 등록금 관계 확인 scatter plot
sns.scatterplot(data = df, x = "등록금", y = "수업료")
plt.show()