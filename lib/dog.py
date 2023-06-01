import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    #init method/ constructor 

    def __init__(self, name, breed, id=None): 
        self.name = name
        self.breed = breed
        self.id = id 
    pass


    @classmethod
    def create_table(cls): 
        query = """CREATE TABLE IF NOT EXISTS dogs(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    breed TEXT
                    )"""

        CURSOR.execute(query)

    @classmethod
    def drop_table(cls): 
        query =  """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(query)

    #instance method  / not a class method 
    def save(self):
        query = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?);
        """

        CURSOR.execute(query, (self.name, self.breed))

    #class method 
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed) #create an instance 

        dog.save() #take the save method that we built earlier to inert into our table

        return dog
    
    #grabbing one row
    @classmethod
    def new_from_db(cls, row):
        dog = cls(
            id = row[0],
            name = row[1],
            breed = row[2]
        )

        print(dog.name, dog.breed)
        return dog
    

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs 
        """

        print([ cls.new_from_db(one_row) for one_row in CURSOR.execute(sql).fetchall()])
        return [ cls.new_from_db(one_row) for one_row in CURSOR.execute(sql).fetchall()]

Dog.drop_table()
Dog.create_table()
dog1 = Dog("Honey", "Chihuahua", 1)
dog2 = Dog("Milk", "Chihuahua2", 2)
dog3 = Dog("Ginger", "Chihuahua3", 3)
print(dog1.save())
print(Dog.create("joey", "cocker spaniel"))
Dog.create("joey", "cocker spaniel")
dog2.save()
dog3.save()
print(Dog.get_all())
