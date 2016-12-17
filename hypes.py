import psycopg2 as dbapi2

class Hype:
    def __init__(self, app):
        self.app = app

    def Initialize_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """CREATE TABLE IF NOT EXISTS HYPES (
                           HYPE_ID         SERIAL        PRIMARY KEY    NOT NULL,
                           USER_ID         INT                          NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                           DATE            DATE                         NOT NULL,
                           TEXT            VARCHAR(150)                 NOT NULL,
                           TOPIC           VARCHAR(20)                  NOT NULL
                           )"""
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Drop_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "DROP TABLE IF EXISTS HYPES"
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Initialize_Comments(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """CREATE TABLE IF NOT EXISTS COMMENTS (
                           COMMENT_ID      SERIAL    PRIMARY KEY   NOT NULL,
                           HYPE_ID         INT       REFERENCES    HYPES(HYPE_ID)    ON DELETE CASCADE,
                           USER_ID         INT                     NOT NULL,
                           DATE            DATE                    NOT NULL,
                           TEXT            VARCHAR(150)            NOT NULL
                           )"""
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Drop_Comments(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "DROP TABLE IF EXISTS COMMENTS"
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Add_Hype(self, userID, t, text, topic):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO HYPES(
                           USER_ID,
                           DATE,
                           TEXT,
                           TOPIC)
                           VALUES("""+ str(userID) +",'" + str(t) +"','"+ text +"','"+ topic +"' )"
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def Get_Hype_ID(self, userID, t, text, topic):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT HYPE_ID FROM HYPES WHERE USER_ID = '"+ str(userID) +"' AND DATE='" + str(t) +"' AND TEXT='"+ text +"' AND TOPIC='"+ topic +"'"
                cursor.execute(query)
                hype_ID = cursor.fetchone()
                return hype_ID[0]
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def Select_All_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM HYPES ORDER BY HYPE_ID"
                cursor.execute(query)
                hypes = cursor.fetchall()
                return hypes
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def Comment_Hype(self, hypeID, userID, t, text):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO COMMENTS(
                HYPE_ID,
                USER_ID,
                DATE,
                TEXT)
                VALUES("""+ str(hypeID) +", "+ str(userID) +",'" + str(t) +"','"+ text + "' )"
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()
