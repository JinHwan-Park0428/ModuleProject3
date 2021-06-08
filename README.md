# ModuleProject3
Kafka, Scrapy, Mysql, Django를 Python을 이용하여 데이터를 수집하고 가공하여 DB에 저장하고 제공하는 간단한 프로그램을 구현

## Kafka-Stock
Kafka-python을 활용하여 비트코인 주식 정보를 크로울링 하고 Mysql에 저장한 다음 Django-restframework를 활용하여 JsonAPI를 제공한다.
### 제공하는 기능
1. 특정 비트코인의 이름, 가격, 거래량, 일일 변동량 등을 수집하고 제공
2. 사용자로부터 원하는 시간 변수를 받아들여서 특정 시간대의 비트코인 가격 변동, 서로 다른 비트코인 비교 등의 사진을 제공

## Kafak-weather
Kafka-python을 활용하여 전세게 날씨 정보를 크로울링 하고 Mysql에 저장한 다음 Django-restframework를 활용하여 JsonAPI를 제공한다.
### 제공하는 기능
1. 일부 국가의 날씨정보를 수집하고 제공
2. 사용자로부터 원하는 지역 변수 & 시간 변수를 받아들여서 특정 시간대 지역의 날씨 정보를 제공

### 프로젝트에 관련된 자세한 내용은 모듈프로젝트3_박진환.pdf를 참고
