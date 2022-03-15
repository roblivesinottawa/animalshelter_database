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

    def insert_into_animals(self):
        '''inserts data into animals'''
        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                '''
                INSERT INTO	Animals (Name, Species, Primary_Color, Implant_Chip_ID, Breed, Gender, Birth_Date, Pattern, Admission_Date)
                VALUES
                --('Abby', 'Dog', 'Black', 'fdfdb6fe-3347-4e80-8c8a-2e3235c6d1de', NULL, 'F', CAST('1999-02-19' AS DATE), 'Tricolor', CAST('2016-07-19' AS DATE)),
                ('Ace', 'Dog', 'Ginger', '33d50c6b-9d2e-4eb1-8171-0466dee4f349', NULL, 'M', CAST('2005-12-19' AS DATE), 'Bicolor', CAST('2019-06-25' AS DATE)),
                ('Angel', 'Dog', 'Brown', 'f0769a5e-1a11-49f1-ac80-3f40a32ea158', NULL, 'F', CAST('2001-09-19' AS DATE), 'Tuxedo', CAST('2017-02-04' AS DATE)),
                ('April', 'Rabbit', 'Gray', 'ccfef7e8-6fad-4ba0-81ea-0611dd229e42', NULL, 'F', CAST('2005-01-27' AS DATE), 'Broken', CAST('2019-04-24' AS DATE)),
                ('Archie', 'Cat', 'Ginger', '970d7094-ab66-4dca-a0d1-0c16264989af', 'Persian', 'M', CAST('2009-08-26' AS DATE), 'Tricolor', CAST('2016-07-10' AS DATE)),
                ('Arya', 'Dog', 'Gray', 'cd1528ad-c91d-47ea-9b70-3cacd5bdbe71', NULL, 'F', CAST('2014-04-14' AS DATE), 'Bicolor', CAST('2018-06-10' AS DATE)),
                ('Aspen', 'Dog', 'Brown', '51d4cfd1-cd25-4c5a-aa52-0bfd771f8886', NULL, 'F', CAST('2010-04-17' AS DATE), 'Tuxedo', CAST('2016-02-09' AS DATE)),
                ('Bailey', 'Dog', 'Ginger', '36438bc9-e225-4038-97b2-1e28fd287957', NULL, 'F', CAST('2014-09-28' AS DATE), 'Bicolor', CAST('2018-10-01' AS DATE)),
                ('Baloo', 'Rabbit', 'White', 'f5ce3a02-1ec7-431d-8a76-09369e8d798b', 'English Lop', 'M', CAST('2015-04-27' AS DATE), 'Broken', CAST('2016-08-21' AS DATE)),
                ('Beau', 'Dog', 'Cream', '4b94a68c-0c97-4f70-9275-35b3a9eee8d9', NULL, 'M', CAST('2016-02-09' AS DATE), 'Solid', CAST('2017-05-24' AS DATE)),
                ('Benji', 'Dog', 'Gray', '646f0a76-14e4-42e7-9554-3af1ea6cc78f', 'English setter', 'M', CAST('2012-05-21' AS DATE), 'Bicolor', CAST('2018-10-02' AS DATE)),
                ('Benny', 'Dog', 'Brown', '2ae54bbb-a587-49d5-9a4d-1400a303c4bf', NULL, 'M', CAST('2010-03-04' AS DATE), 'Tuxedo', CAST('2018-09-30' AS DATE)),
                ('Blue', 'Dog', 'Ginger', '6d296d1d-e14d-4308-8b4f-27f87fe1534e', NULL, 'M', CAST('2003-09-03' AS DATE), 'Bicolor', CAST('2016-04-03' AS DATE)),
                ('Bon bon', 'Rabbit', 'Gray', 'bce7e239-304a-483d-9e38-05b9b66af496', NULL, 'F', CAST('2002-06-29' AS DATE), 'Broken', CAST('2016-01-03' AS DATE)),
                ('Boomer', 'Dog', 'Black', '01e2ad60-daa5-4681-b934-40c9dcf7d73a', 'Schnauzer', 'M', CAST('2013-08-11' AS DATE), 'Tricolor', CAST('2017-01-11' AS DATE)),
                ('Brody', 'Dog', 'Black', 'eb517826-e48a-41ae-a5fb-1bbeca23c05d', 'Schnauzer', 'M', CAST('2007-08-23' AS DATE), 'Tricolor', CAST('2018-12-05' AS DATE)),
                ('Brutus', 'Dog', 'Ginger', 'b7fad096-7cd1-42a7-85d6-0c3e6599dbeb', 'Weimaraner', 'M', CAST('2011-04-04' AS DATE), 'Bicolor', CAST('2018-08-03' AS DATE)),
                ('Buddy', 'Cat', 'White', '6d49b3f6-e075-4f33-97a3-1d4878ee1345', NULL, 'M', CAST('2017-01-26' AS DATE), 'Tortoiseshell', CAST('2018-12-20' AS DATE)),
                ('Callie', 'Dog', 'Cream', '2636f17f-5893-482f-94a7-47eeb715047a', 'English setter', 'F', CAST('2003-08-28' AS DATE), 'Solid', CAST('2017-12-19' AS DATE)),
                ('Charlie', 'Cat', 'Gray', 'ab967364-43cc-4dd2-a4d9-080f0def56ca', NULL, 'M', CAST('2016-06-16' AS DATE), 'Calico', CAST('2018-02-16' AS DATE)),
                ('Chico', 'Dog', 'Brown', 'c6614119-945a-45a9-a5a2-3c8f840edc01', NULL, 'M', CAST('2014-03-20' AS DATE), 'Tuxedo', CAST('2019-03-22' AS DATE)),
                ('Chubby', 'Rabbit', 'Ginger', '561fea02-9c12-43b1-9ea8-071c9eae4c55', NULL, 'M', CAST('2013-02-07' AS DATE), 'Broken', CAST('2017-10-31' AS DATE)),
                ('Cleo', 'Cat', 'Black', '0897655b-1486-4d5d-ad60-03a855afcaf3', NULL, 'F', CAST('2015-08-13' AS DATE), 'Tortoiseshell', CAST('2019-09-06' AS DATE)),
                ('Cooper', 'Dog', 'Black', '14f9e97b-6cd4-4ee4-9798-1c4f2376141b', NULL, 'M', CAST('2009-11-15' AS DATE), 'Tricolor', CAST('2017-01-15' AS DATE)),
                ('Cosmo', 'Cat', 'Cream', '2754b9c9-5df4-4206-818d-21bdd1a093ed', NULL, 'M', CAST('2017-11-09' AS DATE), 'Solid', CAST('2019-05-13' AS DATE)),
                ('Dolly', 'Dog', 'Gray', 'dbdc4f81-1709-49d6-9f73-1d2099eca35c', NULL, 'F', CAST('2013-09-29' AS DATE), 'Bicolor', CAST('2018-04-27' AS DATE)),
                ('Emma', 'Dog', 'Black', 'bac4c56d-ebb6-43e3-86f3-36506e17f74d', 'Schnauzer', 'F', CAST('2006-12-26' AS DATE), 'Tricolor', CAST('2019-03-28' AS DATE)),
                ('Fiona', 'Cat', 'Gray', '90226140-f54e-419d-82e5-0ea81e0e6384', NULL, 'F', CAST('1999-05-23' AS DATE), 'Calico', CAST('2017-01-13' AS DATE)),
                ('Frankie', 'Dog', 'Gray', 'cc96e651-2f1c-45f8-bce2-26ac8c9868a7', 'English setter', 'M', CAST('2003-09-10' AS DATE), 'Bicolor', CAST('2016-06-20' AS DATE)),
                ('George', 'Cat', 'Brown', '6fefc95e-7d46-4e25-b90a-0ba75f45d972', NULL, 'M', CAST('2001-10-04' AS DATE), 'Bicolor', CAST('2017-11-24' AS DATE)),
                ('Ginger', 'Dog', 'Ginger', '9e241a82-ad77-49dc-ad15-0ac8d2e89dde', NULL, 'F', CAST('2015-11-17' AS DATE), 'Bicolor', CAST('2016-11-27' AS DATE)),
                ('Gizmo', 'Dog', 'Brown', '78556795-4748-447f-a2ce-336b01173a18', NULL, 'M', CAST('2006-01-23' AS DATE), 'Tuxedo', CAST('2019-08-14' AS DATE)),
                ('Gracie', 'Cat', 'Black', '66691184-06b1-4aa8-89b3-0def5fd9fbe1', NULL, 'F', CAST('2007-11-20' AS DATE), 'Spotted', CAST('2017-05-21' AS DATE)),
                ('Gus', 'Dog', 'Cream', '104a1427-d921-4d11-b45c-370c70e1578f', 'English setter', 'M', CAST('2014-10-29' AS DATE), 'Solid', CAST('2016-09-28' AS DATE)),
                ('Hobbes', 'Cat', 'Gray', '8788e7b9-dc20-45ef-8778-0066f60d790d', NULL, 'M', CAST('2002-01-01' AS DATE), 'Spotted', CAST('2016-07-29' AS DATE)),
                ('Holly', 'Dog', 'Cream', 'dd737e6e-3b26-43b4-ad4b-28398602df74', NULL, 'F', CAST('2011-06-13' AS DATE), 'Solid', CAST('2016-12-30' AS DATE)),
                ('Hudini', 'Rabbit', 'Cream', 'de295dd6-502f-43e3-b139-06ceb3fa2128', NULL, 'M', CAST('2018-03-22' AS DATE), 'Brindle', CAST('2019-12-10' AS DATE)),
                ('Humphrey', 'Rabbit', 'Cream', '2a423596-5bf8-41a7-906a-0bd3ea15e17c', 'Belgian Hare', 'M', CAST('2008-12-22' AS DATE), 'Brindle', CAST('2017-12-31' AS DATE)),
                ('Ivy', 'Cat', 'Brown', '0955c70b-a2b6-4d78-8e4b-1f6386ffc763', 'Turkish Angora', 'F', CAST('2013-05-13' AS DATE), 'Spotted', CAST('2018-05-20' AS DATE)),
                ('Jake', 'Dog', 'White', '9209d54c-0238-457b-9922-02171e9df0e6', 'Bullmastiff', 'M', CAST('2011-02-27' AS DATE), 'Tuxedo', CAST('2016-12-14' AS DATE)),
                ('Jax', 'Dog', 'Ginger', '24ad2ed9-e7e6-4571-8a45-3c9361418b07', 'Weimaraner', 'M', CAST('2009-02-06' AS DATE), 'Bicolor', CAST('2017-10-03' AS DATE)),
                ('Kiki', 'Cat', 'Cream', '4e029101-2326-461c-8ff7-0eb809f110cb', NULL, 'F', CAST('2015-07-07' AS DATE), 'Tricolor', CAST('2019-11-16' AS DATE)),
                ('King', 'Dog', 'Brown', '793e68eb-b952-4425-b9e2-0406ea01ac53', NULL, 'M', CAST('2015-09-12' AS DATE), 'Tuxedo', CAST('2017-08-29' AS DATE)),
                ('Kona', 'Dog', 'Gray', 'c87ee041-973f-482c-b5e4-3310b4d80612', NULL, 'F', CAST('2008-10-16' AS DATE), 'Bicolor', CAST('2019-12-13' AS DATE)),
                ('Layla', 'Dog', 'Cream', 'df2e0bbc-acb7-413c-90bc-2aae37aceb90', NULL, 'F', CAST('2006-03-11' AS DATE), 'Solid', CAST('2018-06-14' AS DATE)),
                ('Lexi', 'Dog', 'Brown', 'bfd890aa-afb6-4e8f-b60b-0124840eb504', NULL, 'F', CAST('2017-09-17' AS DATE), 'Tuxedo', CAST('2018-06-22' AS DATE)),
                ('Lily', 'Dog', 'Black', '11de2603-8bcf-49b6-9dde-46f893d93948', 'Schnauzer', 'F', CAST('2001-04-03' AS DATE), 'Tricolor', CAST('2016-06-18' AS DATE)),
                ('Lucy', 'Dog', 'Brown', '3a389eaf-f623-4cd7-9ec9-2144ca9d244c', 'Weimaraner', 'F', CAST('2003-04-04' AS DATE), 'Tuxedo', CAST('2018-02-22' AS DATE)),
                ('Luke', 'Dog', 'Gray', 'fd6e5e29-0515-47a8-890d-096f07c83738', NULL, 'M', CAST('2017-04-23' AS DATE), 'Bicolor', CAST('2017-12-23' AS DATE)),
                ('Lulu', 'Cat', 'Ginger', '9f018ecd-7d17-4027-8751-2167300d6cf3', NULL, 'F', CAST('2003-12-19' AS DATE), 'Calico', CAST('2019-10-09' AS DATE)),
                ('Luna', 'Dog', 'Cream', '74c3566b-a889-4861-b67e-3570aac7247a', NULL, 'F', CAST('2009-01-14' AS DATE), 'Solid', CAST('2017-03-02' AS DATE)),
                ('Luna', 'Rabbit', 'Black', '202c2c7d-7a25-449d-ad71-05482b04346f', NULL, 'F', CAST('2010-11-16' AS DATE), 'Broken', CAST('2017-08-18' AS DATE)),
                ('Mac', 'Dog', 'Gray', '3b55a74d-c5f7-44bc-9e6a-11c446628a0d', 'English setter', 'M', CAST('2006-12-23' AS DATE), 'Bicolor', CAST('2018-01-03' AS DATE)),
                ('Maddie', 'Dog', 'Brown', '2a37b609-d1f6-475f-a890-0234fcb2f0b8', NULL, 'F', CAST('2014-09-26' AS DATE), 'Tuxedo', CAST('2017-05-02' AS DATE)),
                ('Max', 'Dog', 'Gray', 'eb92c3b9-19bd-4ab1-b0f3-11dd7adb3cf0', NULL, 'M', CAST('2001-12-01' AS DATE), 'Bicolor', CAST('2017-07-26' AS DATE)),
                ('Millie', 'Dog', 'Ginger', '7d69f605-c2ff-42ac-a5ac-20b63eb881ca', NULL, 'F', CAST('2015-05-18' AS DATE), 'Bicolor', CAST('2016-10-27' AS DATE)),
                ('Miss Kitty', 'Cat', 'Black', '1ab8347c-6349-4092-9667-09653a9fd09c', 'Maine Coon', 'F', CAST('2016-09-19' AS DATE), 'Bicolor', CAST('2019-10-19' AS DATE)),
                ('Misty', 'Cat', 'Ginger', '805281a0-5de6-4ba8-8fb1-11cefe0575e0', 'Siamese', 'F', CAST('2009-02-21' AS DATE), 'Spotted', CAST('2019-06-06' AS DATE)),
                ('Mocha', 'Dog', 'Brown', '63dc76e7-3431-4455-9ad8-2fe4ff72f4af', NULL, 'F', CAST('2002-09-23' AS DATE), 'Tuxedo', CAST('2019-01-10' AS DATE)),
                ('Nala', 'Dog', 'Gray', '2929bba7-ed35-43f1-9f3e-01120beb4f8b', 'English setter', 'F', CAST('2018-06-02' AS DATE), 'Bicolor', CAST('2019-07-19' AS DATE)),
                ('Nova', 'Cat', 'White', '81802526-cae2-40bb-846a-01d2156545b4', 'Sphynx', 'F', CAST('2011-04-07' AS DATE), 'Tortoiseshell', CAST('2017-12-09' AS DATE)),
                ('Odin', 'Dog', 'Ginger', 'd6088551-bad5-41f6-b9a5-09a3a50cb2ff', NULL, 'M', CAST('2007-07-10' AS DATE), 'Bicolor', CAST('2016-09-15' AS DATE)),
                ('Oscar', 'Cat', 'White', '18c0c340-e7a3-430e-baf5-13c938287d4f', NULL, 'M', CAST('2008-06-08' AS DATE), 'Bicolor', CAST('2018-02-23' AS DATE)),
                ('Otis', 'Dog', 'Ginger', 'cb5444d8-39fc-4a56-aa83-17e1bfd6e960', NULL, 'M', CAST('2008-05-15' AS DATE), 'Bicolor', CAST('2018-07-22' AS DATE)),
                ('Patches', 'Cat', 'Gray', '21247670-2e5a-43ef-acf9-0e794463c466', NULL, 'F', CAST('2014-07-29' AS DATE), 'Bicolor', CAST('2018-11-04' AS DATE)),
                ('Peanut', 'Rabbit', 'Gray', '99a021d1-5e5a-4499-8759-02b3d89ce9af', NULL, 'M', CAST('2008-10-14' AS DATE), 'Broken', CAST('2018-04-11' AS DATE)),
                ('Pearl', 'Cat', 'Brown', 'df9291b5-9f82-4ad1-a9fd-1206fd6cd837', 'American Bobtail', 'F', CAST('2012-07-05' AS DATE), 'Tricolor', CAST('2019-04-09' AS DATE)),
                ('Penelope', 'Cat', 'Brown', '5a6a4dc1-b813-4331-b027-1718eb50bc9e', 'Scottish Fold', 'F', CAST('2000-09-21' AS DATE), 'Tabby', CAST('2017-07-12' AS DATE)),
                ('Penelope', 'Dog', 'White', 'e4e5609a-9c86-4c59-8eee-47ed74ff04b5', 'Bullmastiff', 'F', CAST('2008-06-28' AS DATE), 'Tuxedo', CAST('2016-01-14' AS DATE)),
                ('Penny', 'Cat', 'Cream', 'b947b10b-c402-4da5-9713-185fd21065c4', NULL, 'F', CAST('2005-11-02' AS DATE), 'Tricolor', CAST('2017-02-15' AS DATE)),
                ('Piper', 'Dog', 'Ginger', 'b6bd98c9-5f0d-4ac2-81ad-278acf2afd46', NULL, 'F', CAST('2012-03-08' AS DATE), 'Bicolor', CAST('2016-03-21' AS DATE)),
                ('Poppy', 'Dog', 'Brown', '10e33eb3-a2d5-4fcd-9428-1dbb389fbb30', 'Weimaraner', 'F', CAST('2011-04-09' AS DATE), 'Tuxedo', CAST('2018-05-05' AS DATE)),
                ('Prince', 'Dog', 'Cream', '06c5cfcb-2c24-4030-acda-06fb3343a173', NULL, 'M', CAST('2016-11-06' AS DATE), 'Solid', CAST('2017-08-29' AS DATE)),
                ('Pumpkin', 'Cat', 'Gray', '64085fe7-0f2e-4e80-a170-286f1519fda8', 'Russian Blue', 'M', CAST('2002-12-28' AS DATE), 'Spotted', CAST('2019-01-18' AS DATE)),
                ('Ranger', 'Dog', 'Ginger', '559412c8-2c13-4a18-8b94-481bc06099de', NULL, 'M', CAST('2015-07-12' AS DATE), 'Bicolor', CAST('2017-09-25' AS DATE)),
                ('Remi / Remy', 'Dog', 'Cream', '835106aa-cfa5-47fb-ba29-0071d1a1592a', NULL, 'M', CAST('2001-08-12' AS DATE), 'Solid', CAST('2018-10-13' AS DATE)),
                ('Riley', 'Dog', 'Ginger', 'e042131e-2921-442c-9bbd-107507293bb2', NULL, 'F', CAST('2013-05-01' AS DATE), 'Bicolor', CAST('2019-03-08' AS DATE)),
                ('Rocky', 'Cat', 'Brown', '6c07246c-3107-4651-8f5c-1eb14d1c5ea5', NULL, 'M', CAST('2009-03-26' AS DATE), 'Solid', CAST('2019-11-18' AS DATE)),
                ('Roxy', 'Dog', 'Brown', '01dfa05c-86b4-4936-a608-1c59097fa2d3', 'Weimaraner', 'F', CAST('2013-03-28' AS DATE), 'Tuxedo', CAST('2018-07-23' AS DATE)),
                ('Rusty', 'Dog', 'Ginger', '92ffde28-b23a-4249-a32d-07ba417aa143', NULL, 'M', CAST('2005-01-27' AS DATE), 'Bicolor', CAST('2016-01-05' AS DATE)),
                ('Sadie', 'Cat', 'Gray', 'c231514d-61c1-4180-b679-0bdba7314fd6', NULL, 'F', CAST('2016-08-24' AS DATE), 'Bicolor', CAST('2016-09-19' AS DATE)),
                ('Salem', 'Cat', 'Ginger', '59f3aa7b-4d2b-49f6-9964-0155880b0473', 'Sphynx', 'M', CAST('2011-02-26' AS DATE), 'Spotted', CAST('2017-10-29' AS DATE)),
                ('Sam', 'Cat', 'Gray', '27f6f2b4-3570-43e1-8b64-05a1dc86fd8d', NULL, 'M', CAST('2016-09-18' AS DATE), 'Bicolor', CAST('2018-10-09' AS DATE)),
                ('Sammy', 'Dog', 'Black', '42d68579-c4be-4dc3-9c35-1c40a9ef7b11', NULL, 'M', CAST('2012-08-24' AS DATE), 'Tricolor', CAST('2018-04-05' AS DATE)),
                ('Samson', 'Dog', 'Ginger', 'a5fa2dc8-9708-465f-9f64-0b39d31be53a', NULL, 'M', CAST('2008-01-24' AS DATE), 'Bicolor', CAST('2018-12-28' AS DATE)),
                ('Shadow', 'Dog', 'Black', '02dc6920-79bd-430a-a1ed-3196366f9bfe', NULL, 'M', CAST('2014-07-09' AS DATE), 'Tricolor', CAST('2016-04-07' AS DATE)),
                ('Shelby', 'Dog', 'Gray', '83f5b5b0-af40-4a45-9bdf-0f8ea289e906', NULL, 'F', CAST('2004-08-04' AS DATE), 'Bicolor', CAST('2016-01-28' AS DATE)),
                ('Simon', 'Cat', 'Gray', '39ed8368-b8bc-433e-8678-0199bce6259e', NULL, 'M', CAST('2008-07-19' AS DATE), 'Bicolor', CAST('2017-10-23' AS DATE)),
                ('Skye', 'Dog', 'White', 'b7db3359-2e5d-42ab-af61-0f1d97ee195c', 'Bullmastiff', 'F', CAST('2013-12-10' AS DATE), 'Tuxedo', CAST('2016-04-20' AS DATE)),
                ('Stanley', 'Cat', 'Cream', '44b218ef-c708-46b7-967e-16c16e4ad577', NULL, 'M', CAST('2005-01-19' AS DATE), 'Tabby', CAST('2019-11-26' AS DATE)),
                ('Stella', 'Dog', 'Cream', '20ccae0a-96ff-43c1-9fd4-2cf0916620ed', NULL, 'F', CAST('2005-03-11' AS DATE), 'Solid', CAST('2017-02-18' AS DATE)),
                ('Thomas', 'Cat', 'Brown', '265151dd-f5f0-4dcb-a0e7-0371960d9741', NULL, 'M', CAST('2002-12-11' AS DATE), 'Tricolor', CAST('2018-08-04' AS DATE)),
                ('Thor', 'Dog', 'Black', 'ed0ba7ee-6694-452f-92ab-19bd52a750df', NULL, 'M', CAST('2011-05-28' AS DATE), 'Tricolor', CAST('2016-07-24' AS DATE)),
                ('Tigger', 'Cat', 'Brown', '6f39f088-a2ea-40fc-9f7e-0dea387a5b59', 'Turkish Angora', 'M', CAST('2005-06-07' AS DATE), 'Tabby', CAST('2016-01-18' AS DATE)),
                ('Toby', 'Cat', 'Gray', 'e16f5ab8-9e18-4f58-adf8-00be13e5efa0', NULL, 'M', CAST('2012-04-07' AS DATE), 'Spotted', CAST('2019-08-30' AS DATE)),
                ('Toby', 'Dog', 'White', 'a457d717-2c6b-4ad2-8383-3974df128d4f', 'Bullmastiff', 'M', CAST('2003-10-05' AS DATE), 'Tuxedo', CAST('2019-05-08' AS DATE)),
                ('Toby', 'Rabbit', 'White', '01dd3b07-ebd6-4a7f-98bc-0a38aa48b139', NULL, 'M', CAST('2011-10-27' AS DATE), 'Broken', CAST('2019-05-23' AS DATE)),
                ('Tyson', 'Dog', 'Gray', '193e62eb-31cc-49ae-ad45-46cb9cee0efa', NULL, 'M', CAST('2016-01-09' AS DATE), 'Bicolor', CAST('2018-08-19' AS DATE)),
                ('Walter', 'Dog', 'Cream', '293ae36f-bfbe-4ebc-b90c-4a2be6055cd1', NULL, 'M', CAST('2001-12-24' AS DATE), 'Solid', CAST('2016-02-21' AS DATE)),
                ('Whitney', 'Rabbit', 'Black', 'f8fc5dfc-b0f1-4c91-ad34-06d16f2dea33', 'Lionhead', 'F', CAST('2017-03-02' AS DATE), 'Broken', CAST('2017-09-08' AS DATE));
    '''
            )
            self.conn.commit()
            print('data inserted successfully into animals table')
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('error inserting data into animals table')




if __name__=='__main__':
    animal_shelter = AnimalShelter()
    animal_shelter.connection()
    # animal_shelter.create_database('animalshelter')
    # animal_shelter.create_tables()
    # animal_shelter.insert_into_schemas()
    animal_shelter.insert_into_animals()


