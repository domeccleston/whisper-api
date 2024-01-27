import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def main(filename, transcript):
    connection_string = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    
    # Correctly format the SQL query with string values
    cursor.execute("INSERT INTO transcriptions (filename, transcription) VALUES (%s, %s);", (filename, transcript))
    
    # As this is an INSERT operation, there's no need to fetch a record
    connection.commit()
    cursor.close()
    connection.close()

    # Since we're not fetching anything, we can't print the first podcast here
    print(f"Inserted podcast with filename: {filename}")


main("test_podcast_2", "Hello, world")
