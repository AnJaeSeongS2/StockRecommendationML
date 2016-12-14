import StockCode
codes =StockCode.StockCode()
codes.parseCodeHTML(codes.downloadCode(1),1).dumpAll()
#codes.parseCodeHTML(codes.downloadCode(2),2).dumpAll()
print key, value in codes.iterItems()

