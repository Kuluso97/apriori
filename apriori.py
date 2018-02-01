import sys
import time
from collections import defaultdict

def getTransactionListAndItemSet(dataSet):
	inputFile = open(dataSet)
	transactionList = []
	itemDict = defaultdict(int)

	for line in inputFile:
		transaction = frozenset(line.split())
		transactionList.append(transaction)
		for item in transaction:
			itemDict[item] += 1

	return transactionList, itemDict

def getCandidateSet(freqSet, length):
	return set([i.union(j) for i in freqSet for j in freqSet if len(i.union(j)) == length])

def printAnswer(resultList):
	for item in resultList:
		s = ""
		for i in item[0]:
			s += i + ' '
		s += '({0})'.format(item[1])
		print(s)

def main():
	t0 = time.time()
	dataSet, ms = sys.argv[1:]
	ms = int(ms)

	transactionList, itemDict = getTransactionListAndItemSet(dataSet)
	freqSet = set(frozenset([i]) for i in itemDict if itemDict[i] >= ms)
	resultList = [(frozenset([i]),j) for i, j in itemDict.items() if j >= ms]
	
	length = 2

	while freqSet:
		candidateSet = getCandidateSet(freqSet, length)
		localDict = defaultdict(int)
		for transaction in transactionList:
			for candidate in candidateSet:
				if candidate < transaction:
					localDict[candidate] += 1

		freqSet = set(frozenset(i) for i in localDict if localDict[i] >= ms)
		resultList += [(i,j) for i, j in localDict.items() if j >= ms]
		length += 1

	printAnswer(resultList)

	t1 = time.time()
	print(t1-t0)

if __name__ == '__main__':
	main()
