import decisiontree
from helpers import defaultdict,argv,stdout,join,getcwd

def printErr():
	execName=argv[0]
	print 'Usage: python',execName,'--option value --otheroption othervalue [...]'
	print
	print 'default options: --train WORKING_DIR --test WORKING_DIR'
	print
	print 'Options:'
	print '--load tree_file'
	print '\tload the specified tree'
	print '--train directory (chainable)'
	print '\ttrain the tree; directory must contain trainData.csv and trainLabels.csv; if attrNames.csv exists, it will be used to convert the attribute numbers into their respective names when printed'
	print '\tif a tree is already loaded or trained, training data will be inserted and then the tree will be trained from that point'
	print '\totherwise, a new tree will be grown from the training data'
	print '--maxEntropy val'
	print '\tset the maximum entropy allowed in the tree after each training (default: 0)'
	print '--maxPValue val'
	print '\tset the maximum p-value for which a node will be split (default: 1)'
	print '--maxSamples val'
	print '\tcap the input at val samples maximum'
	print '--maxAttrs val'
	print '\tcap the input at val attributes per sample'
	print '--save_tree file'
	print '\tsave the tree in the specified file; save_tree def saves the tree in the working directory'
	print '--save_tree_ascii file'
	print '\tsave the ascii display of the tree in the specified file; save_tree_ascii def saves the tree in the working directory'
	print '--test directory (chainable)'
	print '\ttest the tree on testing data; directory must contain testData.csv and testLabels.csv'
	print '--classify file (chainable)'
	print '\tuse the tree to classify the data in file'
	print '--save_classifications file'
	print '\tappend the classification results to the specified file; save_classifications def saves the output in the working directory (default: stdout)'

args=defaultdict(list)
try:
	for index in xrange(1,len(argv),2):
		args[argv[index][2:]].append(argv[index+1])
except:
	printErr()
	quit()

arglist=['load','train','maxEntropy','maxPValue','maxSamples','maxAttrs','save_tree','save_tree_ascii','test','classify','save_classifications']
for arg in args:
	if not arg in arglist:
		print 'Invalid option:',arg
		printErr()
		quit()
if 'maxEntropy' in args:
	maxEnt=float(args['maxEntropy'][0])
else:
	maxEnt=0.0

if 'maxPValue' in args:
	maxPValue=float(args['maxPValue'][0])
else:
	maxPValue=1.0

if 'maxSamples' in args:
	maxSamples=int(args['maxSamples'][0])
else:
	maxSamples=None

if 'maxAttrs' in args:
	maxAttrs=int(args['maxAttrs'][0])
else:
	maxAttrs=None

def trainTree(tDir='.'):
	tFile=open(join(tDir,'trainData.csv'),'r')
	lFile=open(join(tDir,'trainLabels.csv'),'r')
	try:
		nFile=open(join(tDir,'attrNames.csv'),'r')
	except:
		nFile=None
	print tDir+':'
	tree.train(tFile,lFile,nFile,maxEnt,maxPValue,maxSamples,maxAttrs)

def saveTree(treefile=join(getcwd(),'tree_maxEnt'+str(maxEnt)+'_maxP'+str(maxPValue)+'_maxSam'+str(maxSamples)+'_maxAttrs'+str(maxAttrs))):
	with open(treefile,'wb') as saveF:
		decisiontree.save(tree,saveF)

def testTree(tDir='.'):
	with open(join(tDir,'testData.csv'),'r') as dataFile:
		with open(join(tDir,'testLabels.csv'),'r') as labelFile:
			print tDir+':',tree.testFile(dataFile,labelFile)

if 'load' in args:
	filename=args['load'][0]
	try:
		with open(filename,'rb') as treeFile:
			tree=decisiontree.load(treeFile)
	except:
		print filename,'could not be loaded!'
		quit()
else:
	print '\nTRAINING\n'
	tree=decisiontree.DecisionTree()
	if 'train' in args:
		for tDir in args['train']:
			trainTree(tDir)
	else:
		tree=decisiontree.DecisionTree()
		trainTree()
		saveTree()
		if not 'test' in args:
			print '\nTESTING\n'
			testTree()

if 'save_tree' in args:
	filename=args['save_tree'][0]
	if filename == 'def':
		saveTree()
	else:
		saveTree(filename)

if 'save_tree_ascii' in args:
	filename=args['save_tree_ascii'][0]
	with (open(join(getcwd(),'tree_maxEnt'+str(maxEnt)+'_maxP'+str(maxPValue)+'_maxSam'+str(maxSamples)+'_maxAttrs'+str(maxAttrs)+'_ASCII.txt'),'w') if filename == 'def' else open(filename,'w')) as saveFile:
		saveFile.write(str(tree))

if 'test' in args:
	print '\nTESTING\n'
	for testDir in args['test']:
		testTree(testDir)

if 'classify' in args:
	print '\nCLASSIFYING\n'
	filename=args['save_classifications'][0]
	if filename == 'def':
		filename=join(getcwd(),'classification.txt')
	with (open(filename,'a') if 'save_classifications' in args else stdout) as saveFile:
		for classFile in args['classify']:
			with open(classFile,'r') as classFile:
				tree.classifyFile(classFile,saveFile)
