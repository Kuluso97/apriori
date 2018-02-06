# Emory University CS378
# Homework 1
# Yicheng (Jason) Wang
# NetId: ywan693

import sys
import time
from collections import defaultdict
from itertools import combinations

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

def getCandidateSet(freqSet, infreqSet, length):
	cs = set([i.union(j) for i in freqSet for j in freqSet if len(i.union(j)) == length])
	for index, candidate in enumerate(cs):
		for c in combinations(candidate, length - 1):
			if c in infreqSet:
				del cs[index]

	return cs

def printAnswer(resultList):
	for item in resultList:
		print(" ".join(item[0]) + ' (%s)' % (item[1]))

def getFreqSetInfreqSet(itemDict, ms):
	freqSet, infreqSet = set(), set()
	for i,j in itemDict.items():
		if j >= ms:
			freqSet.add(frozenset([i]))
		else:
			infreqSet.add(frozenset([i]))

	return freqSet, infreqSet

def dbpruning(transactionList, infreqSet, length):
	prunedList = []
	for i, transaction in enumerate(transactionList):
		for c in combinations(transaction, length):
			c = frozenset(list(c))
			if c in infreqSet:
				transactionList[i] -=  c
			
		if transactionList[i]:
			prunedList.append(transactionList[i])
	
	return prunedList


def main():
	t0 = time.time()
	dataSet, ms = sys.argv[1:]
	ms = int(ms)

	transactionList, itemDict = getTransactionListAndItemSet(dataSet)
	# freqSet = set(frozenset([i]) for i in itemDict if itemDict[i] >= ms)
	resultList = [(frozenset([i]),j) for i, j in itemDict.items() if j >= ms]

	freqSet, infreqSet = getFreqSetInfreqSet(itemDict, ms)
	transactionList = dbpruning(transactionList, infreqSet, 1)

	length = 2

	while freqSet:
		candidateSet = getCandidateSet(freqSet, infreqSet, length)
		localDict = defaultdict(int)

		if not transactionList:
			break

		for transaction in transactionList:
			for c in combinations(transaction, length):
				c = frozenset(list(c))
				if c in candidateSet:
					localDict[c] += 1

		resultList += [(i,j) for i, j in localDict.items() if j >= ms]
		freqSet, infreqSet = getFreqSetInfreqSet(localDict, ms)
		transactionList = dbpruning(transactionList, infreqSet, length)
		length += 1

	printAnswer(resultList)

	t1 = time.time()
	print("The program runs for %.2f seconds" % (t1-t0))

if __name__ == '__main__':
	main()
