
import random
import datetime
import xlwt

class Sorts:
	def __init__(self):
		#Initialize excel sheet
		wb = xlwt.Workbook()
		style0 = xlwt.easyxf('font: name Arial, color-index black')

		#Possible range of array number
		minNum = 0
		maxNum = 1000
		#don't do more than 10^5 for bubble and insertion
		#don't do more than 10^7 for the rest
		maxNsquaredSize = 10000
		maxSize = 10000000

		#Set array size
		size = 10
		#Set increment
		increment = "0"

		#begin recording time
		programBegin = datetime.datetime.now()

		while size <= maxSize:

			iterationBegin = datetime.datetime.now()
			print "iteration:", 
			print size

			#Create new excel sheet
			ws = wb.add_sheet(str(size))

			#Write titles of each algorithm
			if size <= maxNsquaredSize:
				ws.write(0,0, "Bubble sort")
				ws.write(0,1, "Insertion sort")
			ws.write(0,2, "Quick sort")
			ws.write(0,3, "Heap sort")
			ws.write(0,4, "Merge sort")
			ws.write(0,5, "Radix sort")

			#Write millisecond taken by each algorithm on a new row
			for i in xrange(1,6):
				array = generateRandomArray(size,minNum,maxNum)

				#don't go past this number for nsquared sorting algorithms
				if size <= maxNsquaredSize:
					time = bubblesort(array)
					ws.write(i,0, time, style0)

					time = insertionsort(array)
					ws.write(i,1, time, style0)

				time = quicksort(array)
				ws.write(i,2, time, style0)

				time = heapsort(array)
				ws.write(i,3, time, style0)

				time = mergesort(array)
				ws.write(i,4, time, style0)

				time = radixsort(array)
				ws.write(i,5, time, style0)

			#increment size of array
			increment = incrementArray(increment)
			size += int(increment)

			#save after each sheet, just in case you want to stop program earlier
			wb.save('Data.xls')

			print "Time taken for iteration:",
			print datetime.datetime.now() - iterationBegin
			print

		print "Time taken overall:",
		print datetime.datetime.now() - programBegin

def bubblesort(array):
	a = array[:]
	startTime = datetime.datetime.now()
	length = len(a)

	for i in xrange(0, length-1):
		for j in xrange(0, length-i-1):
			#compare values
			if a[j+1] < a[j]:
				#swap
				a[j], a[j+1] = a[j+1], a[j]

	return getMilliseconds(startTime)


def insertionsort(array):
	a = array[:]
	startTime = datetime.datetime.now()
	length = len(a)

	#This is the ever expanding sorted list
	for i in xrange(1, length):
		temp = a[i]
		j = i
		while j > 0 and temp < a[j-1]:
			#shift everything else to the right
			a[j] = a[j-1]
			j = j - 1

		#place last element over duplicate
		a[j] = temp;

	return getMilliseconds(startTime)


def radixsort(array):
	a = array[:]
	startTime = datetime.datetime.now()


	bucketCount = 10
	#find largest number
	largest = a[0]
	for element in a:
		if element > largest:
			largest = element

	#get amount of digits in largest number
	largestDigit = len(str(largest))


	for digit in xrange(1, largestDigit+1):
		#new bucket each time
		buckets = [[] for x in xrange(bucketCount)]

		#this converts digits into places (units, tens, hundreds)
		division = 10**(digit-1)

		#add elements to bucket
		for element in a:
			# get current digit
			currentDigit = (element//division)%bucketCount
			buckets[currentDigit].append(element)

		#remove elements from bucket
		i = 0
		for bucket in buckets:
			for element in bucket:
				a[i] = element
				i = i + 1


	return getMilliseconds(startTime)


def quicksort(array):
	a = array[:]
	startTime = datetime.datetime.now()

	_quicksort(a)

	return getMilliseconds(startTime)

def _quicksort(a):
	#if sorted already
	if len(a) <= 1:
		return a

	less = []
	more = []
	pivotList = []

	pivot = a[0]

	for element in a:
		if element < pivot:
			less.append(element)
		elif element > pivot:
			more.append(element)
		else:
			pivotList.append(element)

	return _quicksort(less) + pivotList + _quicksort(more)


def mergesort(array):
	a = array[:]
	#print "Performing merge sort..."
	startTime = datetime.datetime.now()
	_mergesort(a)
	return getMilliseconds(startTime)

def _mergesort(a):
	#splits and merges as it goes
	#stop splitting when array size is 1
	if len(a) > 1:
		mid = len(a)//2
		left = a[:mid]
		right = a[mid:]

		_mergesort(left)
		_mergesort(right)

		#compare values from each pair
		i = 0 #left's index
		j = 0 #right's index
		k = 0 #combined list index

		leftLength = len(left)
		rightLength = len(right)

		#look for smallest element in both arrays
		while i < leftLength and j < rightLength:
			if left[i] < right[j]:
				a[k] = left[i]
				i = i + 1
			else:
				a[k] = right[j]
				j = j + 1

			k = k + 1

		while i < leftLength:
			a[k] = left[i]
			i = i + 1
			k = k + 1
		while j < rightLength:
			a[k] = right[j]
			j = j + 1
			k = k + 1


def heapsort(array):
	a = array[:]
	#first step is to heapify ENTIRE array
	startTime = datetime.datetime.now()
	length = len(a)
	heapify(a, length)

	end = length-1

	#as long as the array is not sorted
	while end > 0:
		#swap
		a[end],a[0] = a[0],a[end]
		#keep reducing array size
		end = end - 1
		#fix all switched parents
		siftDown(a, 0, end)

	return getMilliseconds(startTime)


#Credit to Rosetta code
def heapify(a, length):
	#get last parent node (remember, 0 is first element)
	start = (length-2)//2

	while start >= 0:
		siftDown(a, start, length-1)
		start = start -1

def siftDown(a, start, end):
	root = start
	#as long as there is a left node.. again remember 0 is first element
	while (root*2+1) <= end:
		child = root*2+1
		#if there is a right child and its value is greater...
		if child + 1 <= end and a[child+1] > a[child]:
			#then care about the right child
			child = child + 1
		#if child element is greater than parent..
		if a[child] > a[root]:
			#swap
			a[root], a[child] = a[child], a[root]
			#continue sifting down the tree
			root = child
		else:
			#otherwise we are done sifting
			return

def incrementArray(inc):
	if inc[:1] == "4":
		return "5" + inc[1:]
	if inc[:1] == "5":
		return "4" + inc[1:] + "0"
	if inc[:1] == "0":
		return "40"

def getMilliseconds(startTime):
	c = datetime.datetime.now() - startTime
	milliseconds = (c.days * 24 * 60 * 60 + c.seconds) * 1000 + c.microseconds / 1000.0
	return milliseconds

def generateRandomArray(size, minimum, maximum):
	array = [None] * size

	for i in range(len(array)):
		array[i] = random.randint(minimum, maximum)

	return array

s = Sorts()