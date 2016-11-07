import string
import sys
import os
import codecs
import unicodedata

class translate:

	def translateGIB(GIBstring):	
	
		moves = []
		
		body = False
		
		# I don't like gib files
		while(GIBstring != None):
			first = GIBstring.read(1)
			if(first != 'S'):
				next = GIBstring.read(2)
				if(next == 'GE'):				# this is the eof
					GIBstring = None
					break
				metadata = GIBstring.readline()
				if(next == '[W'):
					splitmeta = metadata.replace(':',',').split(',')
					whitePlayer = splitmeta[5]
				if(next == '[B'):
					splitmeta = metadata.replace(':',',').split(',')
					blackPlayer = splitmeta[5]
			elif(first == 'S'):                  # read a move from file
				body = True
				line = GIBstring.readline()
				splitLine = line.split()
				if (splitLine[0] == 'TO'):
					color = splitLine[3]
					moveX = int(splitLine[4])
					moveY = int(splitLine[5])
					moves.append((color, moveX, moveY))
			   # try again next line
				
		# PB[nathan9 ]BR[3D]PW[sidae777 ]WR[3D]
		SGFstring = '(;GM[1]FF[4]CA[UTF-8]SZ[19]PB[%s]PW[%s]' % (blackPlayer, whitePlayer)
		
		for move in moves:
			if (move[0] == '1'):
				SGFstring += ';B['
			elif (move[0] == '2'):
				SGFstring += ';W['
			else:
				return "Error"
			
			SGFstring += '%s%s]' % (chr(move[1] + 97),chr(move[2] + 97)) # go from number to letter representation with ascii offset for 'a'
		  
		SGFstring += ')'  
		return SGFstring
		
	rootDir = sys.argv[1]
	targetDir = sys.argv[2]
  	
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			if fname.endswith('.gib'):
				print("Cpnverting %s" %fname)
				path = os.path.join(dirName, fname)
				with open(path, mode='rt', encoding="utf-8", errors="ignore") as infile:
					sgfBody = translateGIB(infile)
				writePath = targetDir + dirName[len(rootDir):]
				if not os.path.exists(writePath):
					os.makedirs(writePath)
				writefname = fname[:-4] + '.sgf'
				with open(writePath + '/' + writefname, 'w') as f:
					f.write(sgfBody)
			else:
				continue

		