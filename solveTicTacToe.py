import random
import copy

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

		self.playerIndex = 'HM'

		"""
		boardNum = random.choice(['A','B','C'])
		pos = random.randint(0,8)
		self.latestPosition = (boardNum, pos)
		self.placeTo(boardNum, pos)
		"""
		self.latestPosition = ('None', 0)

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
		self.latestPosition = boardNum + str(pos)

	def isOkToPlace(self, boardNum='A', pos=0):
		if self.isDead(boardNum):
			return False
		if self.board[boardNum][pos/3][pos%3] == 'X':
			return False
		return True

	def aiPlace(self):
		while True:
			boardNum = random.choice(['A','B','C'])
			pos = random.randint(0,8)
			if self.isOkToPlace(boardNum, pos):
				break
		self.placeTo(boardNum, pos)
		
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

class ReflexAgent():
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
			for action in actions:
				if oneBoardMinimaxAgent.getAction(gameState.generateSuccessor(0, action)) == 1:
					aFlag = True
				if isOne(gameState.generateSuccessor(0, action).board):
					oneFlag = True
			if aFlag and oneFlag and countX(boardN)>=2:
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

	def evaluationFunction(self, currentGameState, action):
		successorGameState = currentGameState.generateSuccessor(action)
		fingerPrint_A = self.fingerPrint(successorGameState.board['A'])
		fingerPrint_B = self.fingerPrint(successorGameState.board['B'])
		fingerPrint_C = self.fingerPrint(successorGameState.board['C'])
		multiplyValue = self.multiply(fingerPrint_A, fingerPrint_B, fingerPrint_C)
		if multiplyValue == 'cc' or multiplyValue == 'a' or multiplyValue == 'bb' or multiplyValue == 'bc':
			return 999999
		else:
			return -999999

	def getAction(self, gameState):

		legalMoves = gameState.getLegalActions()

		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		return legalMoves[chosenIndex] #('B', 8)
"""
##Debug
reflexAgent = ReflexAgent()
boardT = [['0','1','2'],
		['3','4','X'],
		['6','7','X']]

print reflexAgent.fingerPrint(boardT)
"""

if __name__ == '__main__':
	game = GameState()
	while not game.isLose():

		#last move is AI move, now it's HM's turn
		if game.playerIndex == 'AI':
			humanInput = raw_input('Your move: ')
			try:
				if game.isOkToPlace(humanInput[0],int(humanInput[1])) and len(humanInput) == 2:
					game.playerIndex = 'HM'
					game.placeTo(humanInput[0],int(humanInput[1]))
					game.display()
				else:
					print 'WRONG INPUT!!'
					continue
			except:
				print 'ERROR INPUT!!'
				continue


		#last move is HM move, now it's AI's turn
		#if game.playerIndex == 'HM':
		else: 
			game.playerIndex = 'AI'
			reflexAgent = ReflexAgent()
			action = reflexAgent.getAction(game)
			print game.playerIndex + ': ' + action[0] + str(action[1])
			game.placeTo(action[0], action[1])
			game.display()

	if game.playerIndex == 'AI':
		print 'AI LOSES!!!'
	else:
		print 'You LOSE!!!'






















