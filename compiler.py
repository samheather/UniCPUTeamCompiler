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
		#pass in line number
		compiled += compileLine(line, lineNumber+1)
	print compiled

def compileLine(inputLine, lineNumber):
	tokens = inputLine.split(' ')
	if (len(tokens)!= 2) and not (tokens[0] in standaloneOpcodes):
		raise ValueError('Expected operand for opcode: ' + tokens[0])
	if (debugMode):
		return compileInstruction(tokens[0], lineNumber) + " " \
		+ compileValue(int(tokens[1]), lineNumber) + "\n"
	else:
		return compileInstruction(tokens[0], lineNumber) \
		+ compileValue(int(tokens[1]), lineNumber)

def compileInstruction(instruction, lineNumber):
	if (instruction in compilerDictionary):
		return compilerDictionary[instruction]
	else:
		raise ValueError('Instruction: \"' + instruction + '\" is not a valid ' \
		+ 'instruction, on line number: ' + str(lineNumber))

def compileValue(value, lineNumber):
	if (value < -128) or (value > 127):
		raise ValueError('Value does not fit into 8 bits.  ' \
		+ 'Line number: ' + str(lineNumber))
	return str(bin(value))[2::]

setupAndStart()