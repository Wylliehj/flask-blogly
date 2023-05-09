from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name='Harrison', last_name='Wyllie')
u2 = User(first_name='Ryan', last_name='Sullivan')
u3 = User(first_name='Cody', last_name='Noble')
u4 = User(first_name='Cassidy', last_name='Crumblin')

p1 = Post(title='Dogs', content='Dogs are cool!', user_id=1)
p2 = Post(title='Cats', content='Cats are okay I guess', user_id=2)
p3 = Post(title='League of legends', content='I wish this game had voice chat', user_id=3)
p4 = Post(title='Guitar', content='Martin guitars are my favorite', user_id=4)

db.session.add_all([u1, u2, u3, u4])
db.session.commit()
db.session.add_all([p1, p2, p3, p4])
db.session.commit()