import sqlite3
import json
class Block:
    def __init__(self) -> None:
        pass

    def get_block(email):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute('''
                        SELECT blocklist.block_user,user.name name,user.picture
                        FROM 
                        blocklist
                        LEFT JOIN user
                        on blocklist.block_user = user.email

                        WHERE 
                        blocklist.email =?
                        and
                        user.name IS NOT NULL
                    
                    
                    ''', (email,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        results=[]
        for row in rows:
            results.append({
                'block_user': row[0],
                'name': row[1],
                'picture':row[2]
            })
        return json.dumps(results)
    
    def add(email,block_user):
        if email!=block_user:
            conn = sqlite3.connect('source/movie.db', timeout=10)
            cursor = conn.cursor()

            insert_query = '''
                            INSERT INTO blocklist (email,block_user) 
                            VALUES (?, ?)
                            '''
            
            user_data = (email, block_user)
            
            cursor.execute(insert_query, user_data)
            conn.commit()
            cursor.close()
            conn.close()