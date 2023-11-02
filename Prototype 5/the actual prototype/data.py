import sqlite3

class save_data():
    def __init__(self):
        self.name = ""
        self.character_name = ""
        self.level_number = -1
        self.unlocked_raditz = False
        self.unlocked_frieza = False
        self.unlocked_cell = False
        self.conn = sqlite3.connect("player_data.sqlite")
        self.c = self.conn.cursor()

    def get_name(self): return self.name
    def set_name(self,a): self.name = a

    def get_character_name(self): return self.character_name
    def set_character_name(self,a): self.character_name = a

    def get_level_number(self): return self.level_number
    def set_level_number(self,a): self.level_number = a

    def select_raditz(self): return self.unlocked_raditz
    def select_frieza(self): return self.unlocked_frieza
    def select_cell(self): return self.unlocked_cell
    

    def get_player_id(self):
        SQL = "SELECT player_id FROM Players WHERE Players.name = '%s'" %(self.get_name())
        for row in self.c.execute(SQL):
            playerID = row[0]
        return playerID
        
        
    def set_characters_unlocked(self):
        if self.get_level_number() >= 1:
            self.unlocked_raditz = True

        if self.get_level_number() >= 2:
            self.unlocked_frieza = True

        if self.get_level_number() == 3:
            self.unlocked_cell = True
            

    def create_tables(self):
        self.c.execute("CREATE TABLE Players(player_id integer primary key autoincrement, name text unique)")

        self.c.execute("CREATE TABLE Attempts(attempt_id integer primary key autoincrement,playerID integer,character_name text,level_number integer, FOREIGN KEY (playerID) REFERENCES Players(player_id))")

        self.conn.commit()

    def load_data(self):
        #set the player name before this
        try:
            SQL = "SELECT character_name, level_number FROM Attempts, Players WHERE Players.name = '%s' AND Players.player_ID = Attempts.playerID ORDER BY level_number" %(self.get_name())
            #order by level number so that the highest number is last
            for row in self.c.execute(SQL):
                if row[1] != self.get_level_number():
                    self.set_character_name(row[0])
                    self.set_level_number(row[1])
        except:
            pass



    def check_data(self):
        SQL = "SELECT name FROM Players"
        for row in self.c.execute(SQL):
            player_name = row[0]
        #if this errors, tables aren't there

        #showing attempts data - for testing
        SQL = "SELECT * FROM Attempts"
        for row in self.c.execute(SQL):
            ID = row[0]
            player_id = row[1]
            character_name = row[2]
            level_number = row[3]
            #print("ID: %d, Player ID: %d, Character: %s, Highest levl: %d" %(ID, player_id,character_name, level_number ))

    def save(self):
        name = None
        #checking if the player is already in the player table
        SQL = "SELECT * FROM Players WHERE name = '%s'" %(self.get_name())
        for row in self.c.execute(SQL):
            name = row[1]
            playerID = row[0]
            
            
        if name == None:
            SQL ="INSERT INTO Players VALUES (NULL, '%s')" %(self.get_name())

            self.c.execute(SQL)
            self.conn.commit()

        #adding the attempt to the attempt table
        SQL = "INSERT INTO Attempts(attempt_id,playerID,character_name,level_number) VALUES(NULL,%d,'%s',%d)" %(self.get_player_id(), self.get_character_name(), self.get_level_number())

        self.c.execute(SQL)
        self.conn.commit()

def check_data():
    data = save_data()
    try:
        data.check_data()
    except:
        data.create_tables()

    return data

    
            

        
        
    
        
