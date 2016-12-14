# StockRecommendation
# 0. DB가 없으면 실행이 안됩니다... DataReadWriter.py내부의 db.connect부분이 개발자에 맞춰져 있습니다.
# 1. tensorflow를 실행하시고 python으로 작성한 실행파일들을 실행합니다. 
# 2. 주식데이터를 갱신해주려면 $python runDownloadStockData.py 실행을 해서 Koscom에서 상장회사 정보를, yahoo Finance에서 일일 주가데이터를 가져옵니다.
# 3. 평균회귀 성향을 계산하려면 $python runCheckMeanReversion.py 실행을 해서 DB에 저장된 주식데이터로 평균회귀성향을 계산한 뒤 DB에 예측한 동향을 저장합니다.
# 4. 동향을 바탕으로 모의투자 결과를 계산하려면 $python runCreateStockPrediction.py 실행을 해서 DB에 모의투자 결과로 적중횟수를 저장합니다.
# 5. 모의투자 결과를 확인하려면 $python runShowStockPrediction.py 실행을 해서 결과종합과 원하는 날짜의 주식동향예측을 보여준다.
# 2~5는 각각 아무때나 원하는 것을 실행해도 잘 동작합니다.
