#! python3
import json
import requests

class Game:
	def __init__(self, server_url, uid):
		action = '/session'
		data = {'uid': uid}
		session = requests.Session()
		res = session.post(url=server_url+action, data=data).json()
		self.token = res['token']
		self.server_url = server_url

	def get_state(self):
		action = '/game'
		params = {'token': self.token}
		session = requests.Session()
		res = session.get(url=self.server_url+action, params=params).json()
		self.size = res['maze_size']
		self.maxX = self.size[0]
		self.maxY = self.size[1]
		self.location = res['current_location']
		self.currX = self.location[0]
		self.currY = self.location[1]
		self.status = res['status']
		self.completedLevels = res['levels_completed']
		self.totalLevels = res['total_levels']

	def get_result(self, move):
		action = '/game'
		data = {'action': move}
		params = {'token': self.token}
		session = requests.Session()
		res = session.post(url=self.server_url+action, params=params, data=data).json()
		return res['result']

def solveMaze(y, x):
	maze[y][x] = '*' #mark current location

	if((x != playMaze.maxX - 1) and (maze[y][x+1] != '*')): #East
		moveRes = playMaze.get_result('RIGHT')
		if(moveRes == 'WALL'):
			maze[y][x+1] = '*'
		elif(moveRes == 'SUCCESS'):
			solveMaze(y, x+1)
			playMaze.get_result('LEFT')
		elif(moveRes == 'END'):
			playMaze.completedLevels+=1
			print('You finished maze ' + str(playMaze.completedLevels) + '!')
			if(playMaze.completedLevels == playMaze.totalLevels):
				print('You have finished all the levels!')
				quit()
			quit()

	if((y != playMaze.maxY - 1) and (maze[y+1][x] != '*')): #South
		moveRes = playMaze.get_result('DOWN')
		if(moveRes == 'WALL'):
			maze[y+1][x] = '*'
		elif(moveRes == 'SUCCESS'):
			solveMaze(y+1, x)
			playMaze.get_result('UP')
		elif(moveRes == 'END'):
			playMaze.completedLevels+=1
			print('You finished maze ' + str(playMaze.completedLevels) + '!')
			if(playMaze.completedLevels == playMaze.totalLevels):
				print('You have finished all the levels!')
				quit()
			quit()

	if((x != 0) and (maze[y][x-1] != '*')): #West
		moveRes = playMaze.get_result('LEFT')
		if(moveRes == 'WALL'):
			maze[y][x-1] = '*'
		elif(moveRes == 'SUCCESS'):
			solveMaze(y, x-1)
			playMaze.get_result('RIGHT')
		elif(moveRes == 'END'):
			playMaze.completedLevels+=1
			print('You finished maze ' + str(playMaze.completedLevels) + '!')
			if(playMaze.completedLevels == playMaze.totalLevels):
				print('You have finished all the levels!')
				quit()
			quit()

	if((y != 0) and (maze[y-1][x] != '*')): #North
		moveRes = playMaze.get_result('UP')
		if(moveRes == 'WALL'):
			maze[y-1][x] = '*'
		elif(moveRes == 'SUCCESS'):
			solveMaze(y-1, x)
			playMaze.get_result('DOWN')
		elif(moveRes == 'END'):
			playMaze.completedLevels+=1
			print('You finished maze ' + str(playMaze.completedLevels) + '!')
			if(playMaze.completedLevels == playMaze.totalLevels):
				print('You have finished all the levels!')
				quit()
			quit()

playMaze = Game('http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com', 304917430)
playMaze.get_state()
maze = [[' '] * playMaze.maxX for i in range(playMaze.maxY)]
solveMaze(playMaze.currY, playMaze.currX)
