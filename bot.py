import pexpect as pe
import re
import copy
import random

class GameState():

	def __init__(self):
		self.board = {}
		self.board['A'] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board['B'] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board['C'] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board['T'] = [['0','X','X'],
						['3','X','5'],
						['X','7','8']]

	def display(self):
		#print self.playerIndex + ': ' + self.latestPosition[0] + str(self.latestPosition[1])
		if not self.isDead('A'):
			print 'A:    ',
		if not self.isDead('B'):
			print 'B:    ',
		if not self.isDead('C'):
			print 'C:    ',
		print

		for i in range(3):

			if not self.isDead('A'):
				for j in range(3):
					print self.board['A'][i][j],
				print '',

			if not self.isDead('B'):
				for j in range(3):
					print self.board['B'][i][j],
				print '',

			if not self.isDead('C'):
				for j in range(3):
					print self.board['C'][i][j],
				print '',
			print '\n',
		pass

	def placeTo(self, boardNum='A', pos=0):
		self.board[boardNum][pos/3][pos%3] = 'X'

	def isOkToPlace(self, boardNum='A', pos=0):
		if self.isDead(boardNum):
			return False
		if self.board[boardNum][pos/3][pos%3] == 'X':
			return False
		return True

	def randPlace(self):
		while True:
			boardNum = random.choice(['A','B','C'])
			pos = random.randint(0,8)
			if self.isOkToPlace(boardNum, pos):
				break
		self.placeTo(boardNum, pos)
		return boardNum, pos
		
	def getLegalActions(self):
		legalActions = []
		for boardNum in ['A', 'B', 'C']:
			if not self.isDead(boardNum):
				for i in range(3):
					for j in range(3):
						if self.board[boardNum][i][j] != 'X':
							legalActions.append((boardNum, i*3+j))
		return legalActions

	def generateSuccessor(self, action):
		boardNum = action[0]
		pos = int(action[1])
		successorGameState = copy.deepcopy(self)
		successorGameState.placeTo(boardNum, pos)
		return successorGameState

	def isLose(self):
		if self.isDead('A') and self.isDead('B') and self.isDead('C'):
			return True
		else:
			return False

	def isDead(self, boardNum='A'):
		if self.board[boardNum][0][0] == 'X' and self.board[boardNum][0][1] == 'X' and self.board[boardNum][0][2] == 'X':
			return True
		if self.board[boardNum][1][0] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][1][2] == 'X':
			return True
		if self.board[boardNum][2][0] == 'X' and self.board[boardNum][2][1] == 'X' and self.board[boardNum][2][2] == 'X':
			return True
		if self.board[boardNum][0][0] == 'X' and self.board[boardNum][1][0] == 'X' and self.board[boardNum][2][0] == 'X':
			return True
		if self.board[boardNum][0][1] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][2][1] == 'X':
			return True
		if self.board[boardNum][0][2] == 'X' and self.board[boardNum][1][2] == 'X' and self.board[boardNum][2][2] == 'X':
			return True
		if self.board[boardNum][0][0] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][2][2] == 'X':
			return True
		if self.board[boardNum][0][2] == 'X' and self.board[boardNum][1][1] == 'X' and self.board[boardNum][2][0] == 'X':
			return True
		return False

class OneBoardState():

	def __init__(self, board):
		self.board = board
		self.playerIndex = 0

	def display(self):
		for row in self.board:
			print row

	def placeTo(self, pos = 0):
		self.board[pos/3][pos%3] = 'X'

	def isLose(self):
		if self.board[0][0] == 'X' and self.board[0][1] == 'X' and self.board[0][2] == 'X':
			return True
		if self.board[1][0] == 'X' and self.board[1][1] == 'X' and self.board[1][2] == 'X':
			return True
		if self.board[2][0] == 'X' and self.board[2][1] == 'X' and self.board[2][2] == 'X':
			return True
		if self.board[0][0] == 'X' and self.board[1][0] == 'X' and self.board[2][0] == 'X':
			return True
		if self.board[0][1] == 'X' and self.board[1][1] == 'X' and self.board[2][1] == 'X':
			return True
		if self.board[0][2] == 'X' and self.board[1][2] == 'X' and self.board[2][2] == 'X':
			return True
		if self.board[0][0] == 'X' and self.board[1][1] == 'X' and self.board[2][2] == 'X':
			return True
		if self.board[0][2] == 'X' and self.board[1][1] == 'X' and self.board[2][0] == 'X':
			return True
		return False

	def getLegalActions(self, playerIndex = 0):
		actions = []
		for row in self.board:
			for item in row:
				if item != 'X':
					actions.append(item)
		return actions 

	def generateSuccessor(self, playerIndex, action):
		successorGameState = copy.deepcopy(self)
		successorGameState.placeTo(int(action))
		return successorGameState

class OneBoardMinimaxAgent():

	def __init__(self, depth = 5):
		self.depth = depth

	def evaluationFunction(self, gameState, depth):
		if depth % 2 == 0:
			return -1
		else:
			return 1
	
	def max_choice(self, gameState, depth):
		actions = gameState.getLegalActions(0)
		max_temp = -99999999
		action_temp = None
		for action in actions:
			this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(0, action), depth=depth+1)
			if this_value > max_temp:
				max_temp = this_value
				action_temp = action
		return (max_temp, action_temp)

	def min_choice(self, gameState, depth):
		actions = gameState.getLegalActions(1)
		min_temp = 99999999
		action_temp = None
		for action in actions:
			this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(1, action), depth=depth+1)
			if this_value < min_temp:
				min_temp = this_value
				action_temp = action
		return (min_temp, action_temp)

	def gameOver(self, gameState, depth):
		if gameState.isLose() or depth == self.depth * 2:
			return True
		else:
			return False

	def this_node_choice(self, gameState, depth): 
		if self.gameOver(gameState, depth):
			return (self.evaluationFunction(gameState, depth), None)
		if depth % 2 == 0:
			return self.min_choice(gameState, depth)
		else:
			return self.max_choice(gameState, depth)
	
	def getAction(self, gameState):
		root_min_value, root_min_action = self.this_node_choice(gameState, 0)
		return root_min_value

class Agent():

	def __init__(self):
		self.board = [[],[],[]]
		self.board[0] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board[1] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]
		self.board[2] = [['0','1','2'],
						['3','4','5'],
						['6','7','8']]


	def readScreen(self, screen_str = ''):
		useful_infomation = re.findall('AI:.*?(\w\w)', screen_str, re.S)[0]
		return useful_infomation[0], int(useful_infomation[1])

	def fingerPrint(self, boardN):
		def countX(boardN):
			count = 0
			for row in boardN:
				for item in row:
					if item == 'X':
						count += 1
			return count

		def isDead(boardN):
			if boardN[0][0] == 'X' and boardN[0][1] == 'X' and boardN[0][2] == 'X':
				return True
			if boardN[1][0] == 'X' and boardN[1][1] == 'X' and boardN[1][2] == 'X':
				return True
			if boardN[2][0] == 'X' and boardN[2][1] == 'X' and boardN[2][2] == 'X':
				return True
			if boardN[0][0] == 'X' and boardN[1][0] == 'X' and boardN[2][0] == 'X':
				return True
			if boardN[0][1] == 'X' and boardN[1][1] == 'X' and boardN[2][1] == 'X':
				return True
			if boardN[0][2] == 'X' and boardN[1][2] == 'X' and boardN[2][2] == 'X':
				return True
			if boardN[0][0] == 'X' and boardN[1][1] == 'X' and boardN[2][2] == 'X':
				return True
			if boardN[0][2] == 'X' and boardN[1][1] == 'X' and boardN[2][0] == 'X':
				return True
			return False

		def isOne(boardN):
			if isDead(boardN)\
				or (countX(boardN) == 1 and boardN[1][1] != 'X')\
				or (countX(boardN) == 3 and boardN[0][0] == 'X' and boardN[1][2] == 'X' and boardN[2][1] == 'X')\
				or (countX(boardN) == 3 and boardN[0][2] == 'X' and boardN[1][0] == 'X' and boardN[2][1] == 'X')\
				or (countX(boardN) == 3 and boardN[2][2] == 'X' and boardN[1][0] == 'X' and boardN[0][1] == 'X')\
				or (countX(boardN) == 3 and boardN[2][0] == 'X' and boardN[0][1] == 'X' and boardN[1][2] == 'X'):
				return True
			return False

		def isB(boardN):
			gameState = OneBoardState(boardN)
			oneBoardMinimaxAgent = OneBoardMinimaxAgent()
			actions = gameState.getLegalActions()
			aFlag = False
			oneFlag = False
			bFlag = False
			for action in actions:
				if oneBoardMinimaxAgent.getAction(gameState.generateSuccessor(0, action)) == 1:
					aFlag = True
				if isOne(gameState.generateSuccessor(0, action).board):
					oneFlag = True
				if isB(gameState.generateSuccessor(0, action).board):
					bFlag = True
			if aFlag and oneFlag and not bFlag and countX(boardN)>=2:
				return True
			return False

		if countX(boardN) == 0:
			return 'c'
		if isOne(boardN):
			return '1'
		if countX(boardN) == 1 and boardN[1][1] == 'X':
			return 'cc'
		oneBoardState = OneBoardState(boardN)
		oneBoardMinimaxAgent = OneBoardMinimaxAgent()
		if oneBoardMinimaxAgent.getAction(oneBoardState) == 1:
			return 'a'
		if isB(boardN):
			return 'b'
		return 'Nope'

	def multiply(self, xs = '1', ys = 'a' , zs = 'b'):
		def s2num(s):
			#   1 a b c
			#-->1 3 5 7
			dict = {'1':1, 'a':3, 'b':5, 'c':7, 'cc':49, 'bb':25, 'bc':35}
			if s in dict:
				return dict[s]
			else:
				return 0
		def num2s(num):
			dict = {49:'cc', 3:'a', 25:'bb', 35:'bc'}
			if num in dict:
				return dict[num]
			else:
				return 'Nope'
		x = s2num(xs)
		y = s2num(ys)
		z = s2num(zs)
		xyz = num2s(x*y*z)
		return xyz

	def isOptimal(self, gameState):
		fingerPrint_A = self.fingerPrint(gameState.board['A'])
		fingerPrint_B = self.fingerPrint(gameState.board['B'])
		fingerPrint_C = self.fingerPrint(gameState.board['C'])
		multiplyValue = self.multiply(fingerPrint_A, fingerPrint_B, fingerPrint_C)
		if multiplyValue == 'cc' or multiplyValue == 'a' or multiplyValue == 'bb' or multiplyValue == 'bc':
			return True
		else:
			return False


	def getAction(self, screen_str, gameState):
		move_board, move_pos = self.readScreen(screen_str)
		gameState.placeTo(move_board, move_pos)
		actions = gameState.getLegalActions()
		for action in actions:
			new_gameState = copy.deepcopy(gameState)
			new_gameState.placeTo(action[0], action[1])
			if self.isOptimal(new_gameState):
				gameState.placeTo(action[0], action[1])
				return action[0]+str(action[1])
		action = gameState.randPlace()
		return action[0]+str(action[1])
		

if __name__ == '__main__':
	child = pe.spawn('python solveTicTacToe.py')
	agent = Agent()
	gameState = GameState()
	while True:
		i = child.expect(['Your move:', 'AI LOSES!!!', 'You LOSE!!!'])
		if i == 0:
			output = child.before
			print 'output', output
			#ai_move = re.search('AI:.*?(\w\w)', output).group()
			move = agent.getAction(output, gameState)
			#move = raw_input()
			child.sendline(move)
		elif i == 1:
			print 'Your AI strategy is not optimal'
			break
		elif i == 2:
			print 'Your AI strategy is good'
			break














