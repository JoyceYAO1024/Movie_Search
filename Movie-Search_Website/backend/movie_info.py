import sqlite3
import json
class Movie:
    def __init__(self) -> None:
        pass

    def movie_info(movieid):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT title,id,genres,overview,release_date,runtime,vote_average,Poster,`cast`,crew
                        FROM movie WHERE id = ?
                        ''', (movieid,))
                        
        
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        results = []
        for row in rows:
            results.append({
                'title': row[0],
                'id': row[1],
                'genres':row[2],
                'overview':row[3],
                'release_date':row[4],
                'runtime':row[5],
                'vote_average':row[6],
                'poster':row[7],
                'cast':row[8],
                'crew':row[9]


            })
        return json.dumps(results)