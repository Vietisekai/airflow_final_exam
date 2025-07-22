import json
import glob
import psycopg2

def stage_songs_to_postgres():
    conn = psycopg2.connect("host=postgres dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    song_files = glob.glob('/usr/local/airflow/include/data/song_data/**/*.json', recursive=True)

    for filepath in song_files:
        with open(filepath, 'r') as f:
            data = json.load(f)
            insert_query = """
            INSERT INTO staging_songs (
                num_songs, artist_id, artist_name, artist_latitude, artist_longitude,
                artist_location, song_id, title, duration, year
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = (
                data.get('num_songs'),
                data.get('artist_id'),
                data.get('artist_name'),
                data.get('artist_latitude'),
                data.get('artist_longitude'),
                data.get('artist_location'),
                data.get('song_id'),
                data.get('title'),
                data.get('duration'),
                data.get('year')
            )
            cur.execute(insert_query, values)

    conn.commit()
    cur.close()
    conn.close()


def stage_events_to_postgres():
    conn = psycopg2.connect("host=postgres dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    event_files = glob.glob('/usr/local/airflow/include/data/log_data/**/*.json', recursive=True)

    for filepath in event_files:
        with open(filepath, 'r') as f:
            for line in f:
                data = json.loads(line)

                insert_query = """
                INSERT INTO staging_events (
                    artist, auth, firstname, gender, iteminsession, lastname, length,
                    level, location, method, page, registration, sessionid, song,
                    status, ts, useragent, userid
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                values = (
                    data.get('artist'),
                    data.get('auth'),
                    data.get('firstName'),
                    data.get('gender'),
                    data.get('itemInSession'),
                    data.get('lastName'),
                    data.get('length'),
                    data.get('level'),
                    data.get('location'),
                    data.get('method'),
                    data.get('page'),
                    data.get('registration'),
                    data.get('sessionId'),
                    data.get('song'),
                    data.get('status'),
                    data.get('ts'),
                    data.get('userAgent'),
                    int(data['userId']) if data.get('userId') and str(data['userId']).isdigit() else None
                )
                cur.execute(insert_query, values)

    conn.commit()
    cur.close()
    conn.close()