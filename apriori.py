import sys
from collections import defaultdict

def getTransactionListAndItemSet(dataSet):
	inputFile = open(dataSet)
	transactionList = []
	itemDict = defaultdict(int)

	for line in inputFile:
		transaction = set(line.split())
		transactionList.append(transaction)
		for item in transaction:
			itemDict[item] += 1

	return transactionList, itemDict

def getCandidateSet(freqSet):
	

def main():
	dataSet, ms = sys.argv[1:]
	ms = int(ms)
	resultSet = set()

	transactionList, itemDict = getTransactionListAndItemSet(dataSet)
	freqSet = set(frozenset(i) for i in itemDict if itemDict[i] >= ms)
	resultSet = resultSet.union(freqSet)
	
	while freqSet:
		CandidateSet = getCandidateSet(freqSet)





if __name__ == '__main__':
	main()