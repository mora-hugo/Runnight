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
            port="5432")

    def createTable(self): #Creer les tables si elles n'existent pas
        tables = (
        """
        CREATE TABLE IF NOT EXISTS SCORE (
            name VARCHAR PRIMARY KEY,
            score INT NOT NULL
            )
            """
        )
        self.cursor.execute(tables)
        self.conn.commit()

    def addScore(self,name,score):
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
            VALUES(%s,%s);
            """
            )
            self.cursor.execute(add,(name,score))
            self.conn.commit()
        else: #Si il existe, changer son score
            update = (
            """
            UPDATE SCORE SET score= (%s)
            WHERE name = (%s)
            """
            )
            self.cursor.execute(update,(score,name,))
            self.conn.commit()

    def afficherScore(self): #renvoi un dictionnaire des scores
        BDDSCORE.cursor.execute("select * from SCORE")
        scores = BDDSCORE.cursor.fetchall()
        score_dict = {}
        for score in scores:
            score_dict[score[0]] = score[1]
        return score_dict
""" EXEMPLE ajouter score
BDDSCORE = BDDSCORE()
BDDSCORE.addScore("Lori",100)
"""
""" EXEMPLE afficher les scores
BDDSCORE = BDDSCORE()
print(BDDSCORE.afficherScore())
"""