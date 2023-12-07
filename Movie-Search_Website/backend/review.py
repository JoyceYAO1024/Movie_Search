import sqlite3
import json
import time
class Review:
    def __init__(self) -> None:
        pass

    def get_review(movie_id,email):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT block_user FROM blocklist WHERE email = ?", (email,))
        r = cursor.fetchall()
        blist=[]
        if r:
            for i in r:
                blist+=[i[0]]
        cursor.execute('''
                        SELECT review.email email,movie_id,review,user.name name,user.picture picture, user.background background,review_time time
                        FROM 
                        review 
                        LEFT JOIN user
                        on review.email = user.email

                        WHERE 
                        movie_id = ?
                        and
                        review.email not in ({})'''.format(','.join('?'*len(blist))), (movie_id, *blist))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'email': row[0],
                'movie_id': row[1],
                'review':row[2],
                'name':row[3],
                'picture':row[4],
                'background':row[5],
                'time':row[6]

            })
        
        cursor.close()
        conn.close()
        return json.dumps(results)
    
    def add_review(email,movie_id,review):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        insert_query = '''
                        INSERT INTO review (email,movie_id,review,review_time) 
                        VALUES (?, ?, ?,?)
                        '''
        
        user_data = (email,movie_id,review,formatted_time)
        
        cursor.execute(insert_query, user_data)
        conn.commit()
        cursor.close()
        conn.close()

    def score(point,movie_id):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()

        cursor.execute("SELECT vote_average FROM movie WHERE id = ?", (movie_id,))

        rows = cursor.fetchall()
        
        cursor.execute("SELECT times_of_votes FROM movie WHERE id = ?", (movie_id,))
        times=cursor.fetchall()
        
        before= rows[0][0]
        times=times[0][0]
        res = (before*(times+1)+point)/(times+2)
        times+=1
        cursor.execute("UPDATE movie SET vote_average = ? WHERE id = ?", (res,movie_id))
        cursor.execute("UPDATE movie SET times_of_votes = ? WHERE id = ?", (times,movie_id))
        conn.commit()
        cursor.close()
        conn.close()
        return res
        