import sqlite3

class naomidb:
	_sqlite = None
	_dbfile = None

	def __init__(self, dbfile):
		self._dbfile = dbfile
		try:
			self._sqlite = sqlite3.connect(self._dbfile)
		except:
			print("failed to connect to sqlite db")
			return

	def getInstalledGames(self):
		return self._sqlite.execute("SELECT installed_games.id, games.id as games_id, filename, games.title as game_name, file_hash FROM installed_games JOIN games ON game_id=games.id ORDER BY game_name").fetchall()

	def getInstalledGameByGameId(self, game_id):
		return self._sqlite.execute("SELECT * FROM installed_games WHERE game_id = ? LIMIT 1", [game_id]).fetchone()

	def getInstalledGameByHash(self, file_hash):
		return self._sqlite.execute("SELECT installed_games.id, games.id as game_id, filename, games.title as game_name, file_hash FROM installed_games JOIN games ON game_id=games.id  WHERE file_hash = ? LIMIT 1", [file_hash]).fetchone()

	def getGameAttributes(self, game_id):
		return self._sqlite.execute("SELECT attributes.name as name, attributes_values.value as value FROM game_attributes JOIN attributes ON game_attributes.attribute_id=attributes.id JOIN attributes_values ON attributes_values_id=attributes_values.id WHERE game_id = ?", [game_id]).fetchall()

	def installGame(self, game_id, filename, file_hash):
		self._sqlite.execute("INSERT INTO installed_games(game_id, filename, file_hash) VALUES(?,?,?)", [game_id, filename, file_hash])
		self._sqlite.commit()

	def editGame(self, game_id, filename, file_hash):
		igid = self._sqlite.execute("SELECT id FROM installed_games WHERE file_hash = ?", [file_hash]).fetchone()

		if igid != None and igid[0] > 0:
			# Game already installed, just update the id of the installed entry
			self._sqlite.execute("UPDATE installed_games SET game_id = ? WHERE id = ?", [game_id, igid[0]])
			self._sqlite.commit()
			print("edited. new = ", game_id)
		else:
			self.installGame(game_id, filename, file_hash)
			print('installed')

	def rmInstalledGameById(self, installed_game_id):
		self._sqlite.execute("DELETE FROM installed_games WHERE id = ?", [installed_game_id])
		self._sqlite.commit()

	def purgeInstalledGames(self):
		self._sqlite.execute("DELETE FROM installed_games")
		self._sqlite.execute("VACUUM")
		self._sqlite.commit()

	def getGameList(self):
		return self._sqlite.execute("SELECT id, title FROM games").fetchall()

	def getGameInformation(self, header_title):
		return self._sqlite.execute("SELECT id, title FROM games WHERE header_title = ? LIMIT 1", [header_title]).fetchone()

	def getAttributes(self):
		return self._sqlite.execute("SELECT * FROM attributes").fetchall()

	def getValuesForAttribute(self, attribute_id):
		return self._sqlite.execute("SELECT id, value from attributes_values WHERE attribute_id= ?", [attribute_id]).fetchall()

