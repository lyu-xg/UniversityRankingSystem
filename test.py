from schoolname import affiliationName


test = ['4CE6FC2D', '4FF45383', '4F05DC4B', '0352694C', '0477FFD3', '05E79D01', '0966B229', '4CF99586', '0259891E', '05C86094', '0BF77E37', '0C4400FF', '3333E44B', '00FF56A8', '07CA5884', '03D00B37', '07C34834', '09E3EE34', '4E718DAA', '0D109F83', '0011EAC4', '0134B592', '0A4ACFBD', '04756336', '06CBC4BA', '012C9CDF', '09368EC9', '007D2F41', '0875EA92', '0B46E8A6', '06194FDE', '863BFDE1', '34ED541F', '0C01DCFD', '08EC4F5B', '012E6F4E', '0489A984', '069F11AE', '062D596B', '348EB203', '05282E0D', '026778A2', '07CB626B', '08D7E515', '06DE3FEB', '862ADA3F', '08EF476D', '078A8AE9', '0C2FE58D', '08E4D2D6', '02B09E25', '03FD8454', '04F0A8A0', '09E1988B', '4EC97A4B', '86366AC3', '0AE9651A', '0368E8BE', '0C2C9DD2', '01A8C383', '09676E2E', '00C50601', '07B99BFA', '0112E226', '093456D7', '070DD5D4', '070DD774', '066A71BC', '021CC5D8', '06CB2E98', '012BCF09', '0229448F', '0A97E0C1', '009779A9', '4EF77785', '4F10C1EB', '04F2C66A', '06D35AFB', '4F076E00', '0B00BA67', '099D876D', '0A2FAFA5', '07427AD9', '0267A61E', '0A2510E5', '08702BDB', '0BC2EB17', '34DF872C', '33CD4141', '0532D181', '01124466', '081E3F30', '0B845BA3', '03839B48', '0B78A057', '351E811C', '0B0ADEB6', '4D2B1EE6', '335ED749', '0616AB9C']
train = ['4FF45383', '4CE6FC2D', '0352694C', '4F05DC4B', '0477FFD3', '05E79D01', '05C86094', '4CF99586', '0966B229', '03D00B37', '3333E44B', '0BF77E37', '0C4400FF', '07CA5884', '0D109F83', '09E3EE34', '0259891E', '4E718DAA', '00FF56A8', '0011EAC4']
truetrain = {'03D00B37': 8, '02B09E25':  20, '0966B229':13, '0D109F83': 16, '0C01DCFD':18, '0477FFD3': 6, '0BF77E37': 15, '07CA5884': 19, '4CE6FC2D': 2, '0352694C': 3, '0011EAC4':4, '4E718DAA': 9, '4CF99586': 11, '3333E44B': 14, '4FF45383': 1, '05C86094': 10, '007D2F41': 12, '0C4400FF': 17, '05E79D01': 7, '4F05DC4B': 5}
truetest = {'00FF56A8': 11, '05B090CE': 13, '0966B229': 7, '0C4400FF': 14, '05282E0D': 17, '0477FFD3': 2, '0BF77E37': 20, '07CA5884': 16, '4CE6FC2D': 1, '0352694C':8, '0229448F': 15, '05C86094': 10, '4E718DAA': 9, '4CF99586': 6, '0D109F83': 19, '04756336': 12, '4FF45383': 4, '07C34834': 18, '05E79D01': 5, '4F05DC4B':3}


for i in test:
	print affiliationName[i]

lst =  sorted(truetest,key=truetest.__getitem__)
print "****************"
for i in lst:
	print affiliationName[i]


for i in range(len(lst)):
	if lst[i] in test:
		print "*******************"
		print "in true %d"% (i+1)
		print "in predict %d"% (test.index(lst[i])+1)
	else:
		print "*******************"
		print "false"