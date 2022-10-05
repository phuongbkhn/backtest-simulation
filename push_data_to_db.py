from pandas import DataFrame
import psycopg2
from config import config
from tqdm import tqdm

def connect_n_push_to_db(df:DataFrame):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected!')
		
        # create a cursor
        cur = conn.cursor()
       
	    # execute a statement
        print("Inserting new data to database...")

        for i in tqdm(range(len(df))):
            data = list(df.loc[i])
            added_value = "('{}','{}',{},{},{},{},{},{},'{}','{}',{},{},{},{},{},{})".format(
                    data[0], data[1], data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15])
            sql_command = "INSERT INTO tickdatatable VALUES {};".format(added_value)
            cur.execute(sql_command)

        conn.commit()

        print("Compeleted!")
      
	# close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect_n_push_to_db()