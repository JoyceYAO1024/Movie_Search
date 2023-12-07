import sqlite3
import json
class Search:
    def __init__(self) -> None:
        pass
    def search_movie(name):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute(
                        "SELECT title,id,overview,release_date,runtime,vote_average,Poster FROM movie WHERE LOWER(title) LIKE '%' || ? || '%'"
                        
                        , (name,))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'title': row[0],
                'id': row[1],
                'overview':row[2],
                'release_date':row[3],
                'runtime':row[4],
                'vote_average':row[5],
                'Poster':row[6]
            })
        
        cursor.close()
        conn.close()
        return json.dumps(results)
    
    def search_type(name):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute(
                        "SELECT title,id,overview,release_date,runtime,vote_average,Poster FROM movie WHERE LOWER(genres) LIKE '%' || ? || '%'"
                        
                        , (name,))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'title': row[0],
                'id': row[1],
                'overview':row[2],
                'release_date':row[3],
                'runtime':row[4],
                'vote_average':row[5],
                'Poster':row[6]
            })
        
        cursor.close()
        conn.close()
        return json.dumps(results)
    
    def search_cast(name):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute(
                        "SELECT title,id,overview,release_date,runtime,vote_average,Poster FROM movie WHERE LOWER(`cast`) LIKE '%' || ? || '%'"
                        
                        , (name,))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'title': row[0],
                'id': row[1],
                'overview':row[2],
                'release_date':row[3],
                'runtime':row[4],
                'vote_average':row[5],
                'Poster':row[6],
            })
        
        cursor.close()
        conn.close()
        return json.dumps(results)
    
    def search_crew(name):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute(
                        "SELECT title,id,overview,release_date,runtime,vote_average,Poster FROM movie WHERE LOWER(crew) LIKE '%' || ? || '%'"
                        
                        , (name,))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'title': row[0],
                'id': row[1],
                'overview':row[2],
                'release_date':row[3],
                'runtime':row[4],
                'vote_average':row[5],
                'Poster':row[6],
            })
        
        cursor.close()
        conn.close()
        return json.dumps(results)