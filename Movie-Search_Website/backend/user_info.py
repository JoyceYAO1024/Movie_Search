import sqlite3
import json

class User:
    def __init__(self) -> None:
        
        pass
    
    def verify(email):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            return False
        else:
            return True
        
    #注册
    def regist(email,password,name):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        insert_query = '''
                        INSERT INTO user (email, password, name, picture, background) 
                        VALUES (?, ?, ?, ?, ?)
                        '''
        
        user_data = (email, password, name, 0, 0)
        
        cursor.execute(insert_query, user_data)
        conn.commit()
        cursor.close()
        conn.close()

    def login(email,password):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM user WHERE email = ?", (email,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            if rows[0][0] == password:
                return True
            else:
                return False
        else:
            return False
    
    def update_picture(email,num):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET picture = ? WHERE email = ?", (num, email))
        conn.commit()
        cursor.close()
        conn.close()

    def update_background(email,num):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET background = ? WHERE email = ?", (num, email))
        conn.commit()
        cursor.close()
        conn.close()

    def get_info(email):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT email,password,name,picture,background FROM user WHERE email = ?", (email,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        results = []
        for row in rows:
            results.append({
                'email': row[0],
                'password': row[1],
                'name':row[2],
                'picture':row[3],
                'background':row[4]
            })
        return json.dumps(results)
    
    def add_wishlist(email,title):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        insert_query = '''
                        INSERT INTO wishlist (email,title) 
                        VALUES (?, ?)
                        '''
        
        user_data = (email, title)
        
        cursor.execute(insert_query, user_data)
        conn.commit()
        cursor.close()
        conn.close()

    def get_wishlist(email):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute('''
                        SELECT wishlist.title id, movie.title name, movie.Poster image
                        FROM wishlist 
                        LEFT JOIN
                        movie
                        on wishlist.title=movie.id
                        WHERE email = ?
                        ''', (email,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        res=[]
        for row in rows:
            res.append({
                'id': row[0],
                'name': row[1],
                'image':row[2]
            })
        return json.dumps(res)
    
    def delete_wishlist(email,title):
        conn = sqlite3.connect('source/movie.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wishlist WHERE email = ? and title= ?", (email,title))
        conn.commit()
        cursor.close()
        conn.close()