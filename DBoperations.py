import psycopg2
from config import *
from reddit import *
import time
import datetime


class DBoperations:

    def __init__(self) -> None:
        self.conn = None
        self.cur = None

    def connect(self) -> None:
        try:

            params = config()
            print("Connecting to postgreSQL database")
            self.conn = psycopg2.connect(**params)

            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError) as error:
            print("Error : ", error)

    def getTrendingRedditData(self):
        self.cur.execute("SELECT NAME FROM STATIC_MARKET_DATA;")
        x = self.cur.fetchall()

        returnList = []
        for i in x:
            returnList.append(str(i)[2: str(i).find(',') - 1])

        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        for coinName in returnList:
            dataFrame = None
            try:
                dataFrame = getSubredditData(coinName)

            except Exception as e:
                print("Error ", e)
            if dataFrame is not None:
                for index, row in dataFrame.iterrows():
                    try:
                        print(row)
                        self.cur.execute(
                            "INSERT INTO REDDIT_DATA(ID, NAME, TIME_STAMP, TITLE, SCORE, SUBREDDIT, URL, NUM_COMMENTS, BODY, CREATED) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                row['id'], coinName, st,
                                row['title'].join(e for e in row['title'] if e.isalnum()).replace("\'", ""),
                                row['score'], row['subreddit'], row['url'],
                                row['num_comments'],
                                row['body'].join(e for e in row['body'] if e.isalnum()).replace("\'", ""),
                                row['created']))

                    except Exception as e:
                        print("ERROR ", e)

                self.conn.commit()


temp = DBoperations()
temp.connect()
temp.getTrendingRedditData()
