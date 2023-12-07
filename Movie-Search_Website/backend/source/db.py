import sqlite3

# 连接到数据库
conn = sqlite3.connect('movie.db')
c = conn.cursor()

# 执行ALTER TABLE语句
c.execute('''ALTER TABLE review ADD COLUMN review_time TEXT DEFAULT '2023-04-21 15:30:45' ''')

# 提交更改
conn.commit()

# 关闭连接
conn.close()