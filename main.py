import psycopg2
from config import config


class AnimalShelter:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.params = config()
        
# this method creates the connection to postgresql database
    def connection(self):
        '''connects to the database'''
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cursor = self.conn.cursor()
            print("Connected to the database")
            print('PostGres Database version:', self.conn.server_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print("Database connection closed")

# this method creates the database
    def create_database(self, database_name):
        '''creates a database in the database'''
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            self.conn.commit()
            print(f"Database {database_name} created")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

# this method creates the tables
    def create_tables(self):
        '''creates tables in the animalshelter database'''
        queries = (
                '''CREATE TABLE Reference.Colors 
                (
                    Color VARCHAR(10) NOT NULL PRIMARY KEY
                );
                ''',
                '''CREATE TABLE Reference.Species 
                (
                    Species VARCHAR(10) NOT NULL PRIMARY KEY
                );''',
                '''
                CREATE TABLE Animals
                (
                    Name VARCHAR(20) NOT NULL,
                    Species	VARCHAR(10)	NOT NULL
                    REFERENCES Reference.Species (Species),
                    Primary_Color VARCHAR(10) NOT NULL
                    REFERENCES Reference.Colors (Color),
                    Implant_Chip_ID	VARCHAR(50)	NOT NULL UNIQUE,
                    Breed VARCHAR(50) NULL,
                    Gender CHAR(1) NOT NULL
                    CHECK (Gender IN ('F', 'M')),
                    Birth_Date DATE NOT NULL,
                    Pattern	VARCHAR(20)	NOT NULL,
                    Admission_Date DATE	NOT NULL,
                    PRIMARY KEY (Name, Species)
                );
                ''',
                '''
                CREATE TABLE Persons
                (
                    Email VARCHAR(100) NOT NULL PRIMARY KEY,
                    First_Name VARCHAR(15) NOT NULL,
                    Last_Name VARCHAR(15) NOT NULL,
                    Birth_Date DATE NULL,
                    Address VARCHAR(100) NOT NULL,
                    State VARCHAR(20) NOT NULL,
                    City VARCHAR(30) NOT NULL,
                    Zip_Code CHAR(5) NOT NULL
                );
                ''',
                '''
                CREATE	TABLE Staff
                (
                    Email VARCHAR(100) NOT NULL PRIMARY KEY REFERENCES Persons(Email), 
                    Hire_Date DATE NOT NULL
                );
                ''',
                '''
                CREATE TABLE Staff_Roles 
                (
                    Role VARCHAR(20) NOT NULL PRIMARY KEY 
                );
                ''',
                '''
                CREATE TABLE Staff_Assignments
                (
                Email VARCHAR(100) NOT NULL REFERENCES Staff (Email) ON UPDATE CASCADE,
                Role VARCHAR(20) NOT NULL REFERENCES Staff_Roles (Role),
                Assigned DATE NOT NULL,
                PRIMARY KEY (Email, Role)
                );
                ''',
                '''
                CREATE	TABLE Adoptions
                (
                    Name VARCHAR(20) NOT NULL,
                    Species VARCHAR(10) NOT NULL,
                    Adopter_Email VARCHAR(100) NOT NULL REFERENCES Persons (Email) ON UPDATE CASCADE,
                    Adoption_Date DATE NOT NULL,
                    Adoption_Fee SMALLINT NOT NULL
                        CHECK (Adoption_Fee >= (0)),
                    PRIMARY KEY (Name, Species, Adopter_Email),
                    FOREIGN KEY (Name, Species) REFERENCES Animals (Name, Species) ON UPDATE CASCADE
                );
                ''',
                '''
                CREATE TABLE Vaccinations
                (
                    Name VARCHAR(20) NOT NULL,
                    Species VARCHAR(10) NOT NULL,
                    Vaccination_Time TIMESTAMP NOT NULL,
                    Vaccine VARCHAR(50) NOT NULL,
                    Batch VARCHAR(20) NOT NULL,
                    Comments VARCHAR(500) NULL,
                    Email VARCHAR(100) NOT NULL REFERENCES Staff (Email) ON UPDATE CASCADE,
                    PRIMARY KEY (Name, Species, Vaccine, Vaccination_Time),
                    FOREIGN KEY (Name, Species)
                        REFERENCES Animals (Name, Species)
                );
                '''
        )
        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cursor = self.conn.cursor()
            [self.cursor.execute(query) for query in queries]
            self.conn.commit()
            print("Tables created")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_into_schemas(self):
        '''inserts data into schemas'''
        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
            '''
            INSERT INTO Reference.Colors (Color)
            VALUES
            ('Black'), ('Brown'), ('Cream'), ('Ginger'), ('Gray'), ('White');
            ''')
            self.conn.commit()
            print("Colors inserted")
            self.cursor.execute(
            '''
            INSERT INTO	Reference.Species (Species)
            VALUES
            ('Cat'), ('Dog'), ('Ferret'), ('Rabbit'), ('Raccoon');
            ''')
            self.conn.commit()
            print("Species inserted")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

            

# this method inserts the data into the tables    
    def insert_data(self, table_name, data : list):
        '''inserts data into a table'''
        try:
            self.cursor.execute(f"INSERT INTO {table_name} VALUES ({data})")
            self.conn.commit()
            print(f"Data inserted into {table_name} successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        

if __name__=='__main__':
    animal_shelter = AnimalShelter()
    animal_shelter.connection()
    # animal_shelter.create_database('animalshelter')
    # animal_shelter.create_tables()
    animal_shelter.insert_into_schemas()
   


