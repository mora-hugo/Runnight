import psycopg2


class BDDSCORE():
    def __init__(self):
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
        self.createTable()

    def connect(self):
        return psycopg2.connect(
            host="ec2-52-31-201-170.eu-west-1.compute.amazonaws.com",
            database="dehn8kd20v1u1v",
            user="axkjwbjpaqmqzn",
            password="aaf8ebb7f3941b151a5cc6a5096346f673d8e8ac8c2eae9cf5ca6da04c683f9e",
            port="5432",
            connect_timeout=10
            )

    def createTable(self): #Creer les tables si elles n'existent pas
        
        tables = (
        """
        CREATE TABLE IF NOT EXISTS SCORE (
            name VARCHAR PRIMARY KEY,
            score INT NOT NULL,
            run INT NOT NULL
            )
            """
        )
        self.cursor.execute(tables)
        self.conn.commit()

    def addScore(self,name,score,run):
        select = ( #Test si le joueur existe dÃ©ja
        """
        SELECT * from score
        WHERE name=%s;
        """
        )
        self.cursor.execute(select,(name,))
        result = self.cursor.fetchone()
        if(result is None): #Si il n'existe pas : l'inserer
            add = (
            """
            INSERT INTO SCORE
            VALUES(%s,%s,%s);
            """
            )
            self.cursor.execute(add,(name,score,run))
            self.conn.commit()
        else: #Si il existe, changer son score
            if score > self.getScore(name):
                update = (
                """
                UPDATE SCORE SET score= (%s), run = (%s)
                WHERE name = (%s)
                """
                )
                self.cursor.execute(update,(score,run,name,))
                self.conn.commit()


    def getScore(self,nom):
        select = ( #Test si le joueur existe dÃ©ja
        """
        SELECT * from score
        WHERE name=%s;
        """
        )
        self.cursor.execute(select,(nom,))
        result = self.cursor.fetchone()
        return result[1]

    def afficherScore(self): #renvoi un dictionnaire des scores


        self.cursor.execute("select * from SCORE ORDER BY score DESC limit 6")
        scores = self.cursor.fetchall()
        score_dict = {}
        for score in scores:
            score_dict[score[0]] = {"score" :score[1], "run" : score[2]}
        return score_dict
""" EXEMPLE ajouter score
BDDSCORE = BDDSCORE()
BDDSCORE.addScore("Lori",100)
"""
""" EXEMPLE afficher les scores
BDDSCORE = BDDSCORE()
print(BDDSCORE.afficherScore())
"""