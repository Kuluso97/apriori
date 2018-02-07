# Emory University CS378
# Homework 1
# Yicheng (Jason) Wang
# NetId: ywan693

import sys
import time
from collections import defaultdict
from itertools import combinations

def loadData(dataSet):
	inputFile = open(dataSet)
	transactionList = []
	itemDict = defaultdict(int)

	for line in inputFile:
		transaction = frozenset(line.split())
		transactionList.append(transaction)
		for item in transaction:
			item = frozenset([item])
			itemDict[item] += 1

	return transactionList, itemDict

def getCandidateSet(freqSet, length):
	return set([i.union(j) for i in freqSet for j in freqSet if len(i.union(j)) == length])

def getFreqUnionSet(freqSet):
	freqUnionSet = set()
	for i in freqSet:
		freqUnionSet = freqUnionSet.union(i)
	return freqUnionSet

def dbpruning(transactionList, freqSet):
	for i, transaction in enumerate(transactionList):
		transactionList[i] = transaction & freqSet

def writeAnswer(resultList, outputFile):
	output = open(outputFile, 'w')
	for item in resultList:
		output.write(" ".join(item[0]) + ' (%s)\n' % (item[1]))

def apriori(dataSet, ms):
	transactionList, itemDict = loadData(dataSet)

	resultList = [(i,j) for i, j in itemDict.items() if j >= ms]
	freqSet = [i for i,j in itemDict.items() if j >= ms]

	freqUnionSet = getFreqUnionSet(freqSet)
	dbpruning(transactionList, freqUnionSet)

	length = 2

	while freqSet:
		candidateSet = getCandidateSet(freqSet,length)	
		localDict = defaultdict(int)
		
		for transaction in transactionList:
			for c in combinations(transaction, length):
				c = frozenset(list(c))
				if c in candidateSet:
					localDict[c] += 1

		resultList += [(i,j) for i, j in localDict.items() if j >= ms]
		freqSet = [i for i,j in localDict.items() if j >= ms]
		freqUnionSet = getFreqUnionSet(freqSet)
		dbpruning(transactionList, freqUnionSet)
		length += 1

	return resultList

def main():
	t0 = time.time()
	if (len(sys.argv) < 4):
		print("You need to type the inputFileName, minimum support and outputFileName on command line")
		sys.exit()

	dataSet, ms, outputFile = sys.argv[1:]
	ms = int(ms)

	resultList = apriori(dataSet, ms)

	writeAnswer(resultList, outputFile)

	t1 = time.time()
	print("The program runs for %.2f seconds" % (t1-t0))

if __name__ == '__main__':
	main()
