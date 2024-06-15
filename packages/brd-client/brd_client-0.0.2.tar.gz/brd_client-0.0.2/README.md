# brd-client



## 설치하기

```bash
pip install brd-client
```



## 사용하기

```python
from brd_client import GoogleSearchAPI

# Google 검색 클라이언트 만들기
google = GoogleSearchAPI(
    country_code="US",
    language_code="en",
    geo_location="New York,United States",
)

################################################################
# 텍스트 검색하기
################################################################
# 전부 검색하기
results = await google.search("bibigo crunchy chicken")

# 기간 제한하여 검색하기 (2024/06/14 이후 수정된 콘텐츠)
results = await google.search("bibigo crunchy chicken", after="2024/06/14")

# 사이트 제한하여 검색하기 (tiktok.com에서만 검색하기)
results = await google.search("bibigo crunchy chicken", site="tiktok.com")

# 최대 검색 결과 300개로 늘리기 (기본 200개)
results = await google.search("bibigo crunchy chicken", max_results=300)

# 텍스트 검색 결과는 리스트 오브 딕셔너리로 되어 있음
# 1개 딕셔너리가 검색 결과 1개 페이지임
# 위 results의 1페이지를 살펴보면 general, input, organic, images, overview, pagination 등의 키를 가지고 있음
results[0].keys()
# dict_keys(['general', 'input', 'organic', 'images', 'overview', 'pagination'])
# general은 검색 소요시간, 검색 시각, 콘텐츠 수 등
# input은 검색 조건
# oraganic은 검색된 콘텐츠 - 주로 봐야하는 것
# images는 이미지 (이미지 검색한 것 아니어도 이미지 몇 개 검색되어 나옴, 브라우저로 Google 검색하는 것과 동일)

################################################################
# 쇼핑, 뉴스, 이미지, 검색하기
# (참고) before, after, site, max_results 파라미터 동일하게 사용 가능
################################################################
# 쇼핑 검색하기
results = google.shopping("bibigo crunchy chicken")

# 뉴스 검색하기
results = google.news("bibigo crunchy chicken")

# 이미지 검색하기
results = google.images("bibigo crunchy chicken")

# 비디오 검색하기
results = google.videos("bibigo crunchy chicken")
```

