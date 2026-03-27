from mongoengine import connect

def init_db():
    connect(
        db= "week3",
        host="mongodb://root:example@localhost:27019/week3?authSource=admin"
    )