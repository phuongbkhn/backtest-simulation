import psycopg2
from config import config
from tqdm import tqdm

tickdata_file = 'tick_data.csv'

def split_info(text):
    extracted_data = []
    split_text = text.split(",")
    for i in split_text:
        split_i = i.split(":")
        extracted_data.append(split_i[1].strip())
    return extracted_data


def connect_n_push_to_db(data:list):
    """ Connect to the PostgreSQL database and Insert new data """
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

        for dt in tqdm(data):
            dt_ = split_info(dt)
            added_value = "('{}','{}',{},{},{},{},{},{},'{}','{}')".format(
                        dt_[0],dt_[1],dt_[2],dt_[3],dt_[4],dt_[5],dt_[6],dt_[7],dt_[8],dt_[9])
            sql_command = "INSERT INTO tickdatatable VALUES {};".format(added_value)
            cur.execute(sql_command)

        conn.commit()

        print("Compeleted! All data is stored in your database!")
      
	# close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    with open(tickdata_file) as f:
        data = f.readlines()
    connect_n_push_to_db(data)