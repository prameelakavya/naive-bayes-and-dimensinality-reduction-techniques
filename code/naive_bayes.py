import pandas, random, math
from collections import OrderedDict

colnames = ["age","job","marital","education","default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","y"]
#bank = pandas.read_csv("bank.csv", names= colnames)
Error = []

for test_runs in range(1):
#################################### TRAINING ###########################################################################
	'''with open("bank.csv") as fr:
		with open("1.csv", "w") as f1, open("2.csv", "w") as f2:
			for line in fr.readlines():
				rd = random.randint(1, 2)
				if rd == 1:
					f = f1
				else:
					f = f2
				f.write(line)

	f.close()
	num_lines_1 = sum(1 for line in open('1.csv'))
	num_lines_2 = sum(1 for line in open('2.csv'))
	if num_lines_2 > num_lines_1:
		bank_test = pandas.read_csv("1.csv", names = colnames)
		bank = pandas.read_csv("2.csv", names = colnames)
	else:
		bank_test = pandas.read_csv("2.csv", names = colnames)
		bank = pandas.read_csv("1.csv", names = colnames)'''

	bank = pandas.read_csv("bank-full.csv", names = colnames)
	bank_test = pandas.read_csv("bank.csv", names = colnames)

	total = len(bank)
	sum_y_yes = 0
	sum_y_no = 0

	for i in list(bank["y"]):
		if i == "no":
			sum_y_no += 1
		else:
			sum_y_yes += 1

	p_y_yes = sum_y_yes/float(total)
	p_y_no = sum_y_no/float(total)

	#print sum_y_yes
	#print sum_y_no


	p_attr = OrderedDict([("age",{}),("job",{}),("marital",{}),("education",{}),("default",{}),("balance",{}),("housing",{}),("loan",{}),("contact",{}),("day",{}),("month",{}),("duration",{}),("campaign",{}),("pdays",{}),("previous",{}),("poutcome",{})])
	#print p_attr
	category = list(bank["y"])

	for i in colnames:
		if i != "y":
			cur_attr = list(bank[i])
			for j in list(set(list(bank[i]))):
				p_attr[i][str(j)] = {"yes" : 0, "no" : 0}
				sum_j_yes = 0
				sum_j_no = 0
				count = 0
				for k in cur_attr:
					if k == j and category[count] == "yes":
						sum_j_yes += 1
					elif k == j and category[count] == "no":
						sum_j_no += 1
					count += 1
				p_attr[i][str(j)]["yes"] = sum_j_yes/float(sum_y_yes)
				p_attr[i][str(j)]["no"] = sum_j_no/float(sum_y_no)

	#print p_attr["contact"]

############################################# TESTING ################################################################

	actual = list(bank_test["y"])

	predicted = []
	test_rows = []
	with open("bank.csv") as f:
		lines = f.readlines()
	f.close()
	for i in lines:
		temp = i.rstrip('\n')
		test_rows.append(temp.split(','))

	#print len(test_rows)
	prod_yes = p_y_yes
	prod_no = p_y_no

	keys_cols = []
	for key in p_attr:
		keys_cols.append(key)


	for i in test_rows:
		for j in range(len(i)-1):
			prod_yes *= p_attr[keys_cols[j]][str(i[j])]["yes"]
			prod_no *= p_attr[keys_cols[j]][str(i[j])]["no"]
		if prod_yes > prod_no:
			predicted.append("yes")
		else:
			predicted.append("no")
		prod_yes = p_y_yes
		prod_no = p_y_no

	#print p_y_no
	#print p_y_yes
#################################################### FINDING ERROR ##########################################################
	
	error = 0
	for i in range(len(actual)):
		if  actual[i] != predicted[i]:
			error += 1
	error_rate = error/float(len(actual))
	Error.append(error_rate)

########################################### Finding mean error and standard deviation ########################################

sum_error = 0
square_sum = float(0)
for i in Error:
	sum_error = sum_error + i

#### variance #######################
mean_error = sum_error/float(len(Error))

for i in Error:
	square_sum += (float(i) - mean_error)^2

variance = square_sum/float(len(Error))


print square_sum/float(len(Error))

print "mean_error                   " + str(mean_error)
print "standard deviation           " + str(math.sqrt(variance))















