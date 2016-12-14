import touch_stock as ts


ts.print_hurst_exponent('samsung.data','samsung2.data','Close')
ts.pprint_adf('samsung.data','Close')

#ts.show_autocorr('samsung.data','Close')
#ts.show_correlogram('samsung.data','Close')
