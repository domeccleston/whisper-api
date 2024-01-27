import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def main(filename, transcript):
    connection_string = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    
    # Correctly format the SQL query with string values
    cursor.execute("INSERT INTO transcripts (filename, transcript) VALUES (%s, %s) RETURNING id;", (filename, transcript))
    
    # Fetch the returned id
    inserted_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    # Since we're not fetching anything, we can't print the first podcast here
    print(f"Inserted podcast with ID: {inserted_id}")


main("test_podcast_4", "some test podcast text")
