import sqlite3 #database 

CONN = sqlite3.connect('lib/dogs.db') #connection
CURSOR = CONN.cursor() #pointer for the connection, row by row 

class Dog:

    # constructor 
    def __init__(self, name, breed, id=None):
        self.id = id #id we dont' know so our default will be None 
        self.name = name
        self.breed = breed 

    @classmethod #affects the whole table, not just one row 
    def create_table(cls): #this class as a parameter 
        #google sql query 
        query = """
            CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT);
        """
        CURSOR.execute(query) # CURSOR takes the 'query' and executes it 
        CONN.commit() #commit this 

    @classmethod
    def drop_table(cls):
        query = """
            DROP TABLE IF EXISTS dogs;

        """
        CURSOR.execute(query) #execute the query 
        CONN.commit() # commit this to the connection

    #instance method / not class method / takes in self / not cls
    def save(self):
        query = """    
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
            """

        # pass in name and breed as arguments / not adding ID 
        CURSOR.execute(query, (self.name, self.breed ))
        #commit
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod 
    def create(cls, name, breed):
        dog = cls(name, breed) #create an instance 

        dog.save() # take save method that we built already and insert into our table 

        return dog # return the dog object 
    
    @classmethod #interacting w/ the whole table 
    def new_from_db(cls, row): # we got this dog class, and one row 
        dog = cls(
            name = row[1], # row at index 1 is name 
            breed = row[2], # row at index 2 is breed
            id = row[0] #row at index 0 is id
        )
        print(dog.name, dog.breed)
        return dog 


    @classmethod
    def get_all(cls):
        sql="""
            SELECT * FROM dogs
        """

        return [cls.new_from_db(one_row) for one_row in CURSOR.execute(sql).fetchall()]
    
    @classmethod
    def find_by_name(cls, name):
        sql="""
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, )).fetchone()

        if not row:
            return None
        
        return Dog(
            name = row[1],
            breed = row[2],
            id = row[0]
        )
