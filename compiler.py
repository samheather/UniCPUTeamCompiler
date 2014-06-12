compilerDictionary = {
						"LOAD" : "00000000",
						"INPUT" : "00000001",
						"READ" : "00100000",
						"WRITE" : "00100001",
						"JUMP" : "00110000",
						"JUMP" : "00110001",
						"JUMP" : "00110010",
						"JUMP" : "00110011",
						"JUMP" : "00010000",
						"ADD" : "00000100",
						"SUB" : "00000101",
						"ADDCY" : "00000110",
						"SUBCY" : "00000111",
						"ADD" : "00100100",
						"SUB" : "00100101",
						"ADDCY" : "00100110",
						"SUBCY" : "00100111",
						"AND" : "00001000",
						"OR" : "00001001",
						"XOR" : "00001010",
						"AND" : "00101000",
						"OR" : "00101001",
						"XOR" : "00101010",
						"SHIFTL" : "00001100",
						"SHIFTR" : "00001110",
						"ROTL" : "00001101",
						"ROTR" : "00001111"
						}

standaloneOpcodes = ["INPUT", "JUMP", "SHIFTL", "SHIFTR", "ROTL", "ROTR"]

# Debug mode > instructions on 1:1 new lines, with space between opcode/operand
# useful for easier readability of outputted code.
debugMode = True

def setupAndStart():
	lines = [line.strip() for line in open('./program.uni')]
	compiled = ""
	for lineNumber, line in enumerate(lines):
		line = line.upper()
		compiled += compileLine(line, lineNumber+1)
	print compiled

def compileLine(inputLine, lineNumber):
	''' str -> str '''
	tokens = removeComment(inputLine).split()

	if len(tokens) == 0:	#comment / whitespace
		return ""
	    
	elif len(tokens) == 1:	#expecting standalone instruction
		if not (tokens[0] in standaloneOpcodes):
			raise ValueError('Expected operand for opcode: ' + tokens[0]) \
			+ 'Line number: ' + str(lineNumber)
		elif (debugMode):
			return compileInstruction(tokens[0], lineNumber) + "\n"
		else:
			return compileInstruction(tokens[0], lineNumber)
		 
	elif len(tokens) == 2:	#expecting standard instruction
		if (tokens[0] in standaloneOpcodes):
			raise ValueError('Unexpected operand for opcode: ' + tokens[0]) \
			+ 'Line number: ' + str(lineNumber)
		elif (debugMode):
			return compileInstruction(tokens[0], lineNumber) + " " \
			+ compileValue(int(tokens[1]), lineNumber) + "\n"
		else:
			return compileInstruction(tokens[0], lineNumber) \
			+ compileValue(int(tokens[1]), lineNumber)

	else:	#too many operands!
		raise ValueError('Unexpected operands for opcode: ' + tokens[0]) \
		+ 'Line number: ' + str(lineNumber)
	
def removeComment(instruction):
	''' str -> str '''
	return instruction.split("//")[0]


def compileInstruction(instruction, lineNumber):
	''' str -> str '''
	if (instruction in compilerDictionary):
		return compilerDictionary[instruction]
	else:
		raise ValueError('Instruction: \"' + instruction + '\" is not a valid ' \
		+ 'instruction, on line number: ' + str(lineNumber))

def compileValue(value, lineNumber):
	''' int -> str '''
	if (value >= 0) and (value <= 127):
		temp = str(bin(value))[2::]
		temp = "".join(bulkBinaryTo8Bits(list(temp)))
		return temp
	elif (value < 0) and (value > -128):
		temp = str(bin(value))[3::]
		# bulk to 8 bits
		temp=binaryComplement(temp) #flip all bits
		temp=binaryIncrement(temp) # now add 1
		temp="".join(temp)
		return temp #bulk this out to 8 bits
	else:
		raise ValueError('Value does not fit into 8 bits.  ' \
		+ 'Line number: ' + str(lineNumber))
		
def bulkBinaryTo8Bits(input):
	'''list -> list'''
	for i in range(0,8-len(input)):
		input.insert(0,'0')
	return input
		
def binaryComplement(input):
	'''str->str'''
	# had to custom write this function since library functions tended towards
	# 32/64/whatever bits repositioning our negation bit.
	input = list(input)
	# first bulk to 8 bits
	input = bulkBinaryTo8Bits(input)
	# now flip
	for t in range(0,len(input)):
		if (input[t] == '0'):
			input[t] = '1'
		else:
			input[t] = '0'
	return "".join(input)
		
def binaryIncrement(input):
	''' str -> str'''
	inputInt = int(input, 2)
	inputInt += 1
	return str(bin(inputInt))[2::]

setupAndStart()
