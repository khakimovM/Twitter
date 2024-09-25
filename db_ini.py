import mysql.connector as connector

DATABASE = "twitter_yangi"


def create_db():
    try:
        conn = connector.connect(
            host="localhost",
            user="root",
            password="aziz1707"
        )
        cur = conn.cursor()

        cur.execute(f"""create database if not exists {DATABASE};""")

        cur.close()
        conn.close()
    except connector.Error as e:
        print("Databasa yaratishda xatolik bor")
        print(e)


def get_connection():
    try:
        return connector.connect(
            host='localhost',
            user='root',
            password='aziz1707',
            database=DATABASE
        )
    except connector.Error as e:
        print("Databasaga ulanishda xatolik bor")
        print(e)


def load_tables():
    create_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""create table if not exists users(
        id int primary key auto_increment,
        name varchar(100),
        username varchar(50) unique,
        email varchar(50) unique,
        password varchar(50)
    );""")

    conn.commit()

    cur.execute("""create table if not exists posts(
        id int primary key auto_increment,
        username varchar(50),
        post varchar(255) unique,
        vaqt datetime default now()
    );""")

    conn.commit()

    cur.execute("""insert ignore into users(name,username,email,password) values
        ('admin','admin','admin@gmail.com','1234'),
        ('Aziz','rayskie','aziz@gmail.com','aziz1707'),
        ('Yaxyo','yaxyo','yaxyo@gmail.com','1234');
    """)

    conn.commit()

    cur.execute("""insert ignore into posts(username, post, vaqt) values
        ('admin', 'Pythonda yangi funksiyalar haqida maqola yozdim.', '2024-09-14 10:30:00'),
        ('rayskie', 'Bugun juda ajoyib dizayn yaratdim!', '2024-09-14 11:00:00'),
        ('yaxyo', 'PyQt5 interfeysini tuzishda qiziqarli yangiliklar bor.', '2024-09-14 11:45:00'),
        ('admin', 'MySQLda optimizatsiya haqida ma’ruza tayyorlayapman.', '2024-09-14 12:00:00'),
        ('rayskie', 'Bugun yangi loyiha haqida rejalashtirish qildik.', '2024-09-14 12:30:00'),
        ('yaxyo', 'AI texnologiyalari haqida o’ylash qiziqarli.', '2024-09-14 13:00:00'),
        ('admin', 'Flask va Django bilan ishlashim davomida topgan muammolarni hal qildim.', '2024-09-14 13:30:00'),
        ('rayskie', 'Boshqaruv paneli dizaynini yangiladim.', '2024-09-14 14:00:00'),
        ('yaxyo', 'Bugun to’liq stack dasturchilik haqida o’rgandim.', '2024-09-14 14:30:00'),
        ('admin', 'Yangi blog maqolasi tayyor.', '2024-09-14 15:00:00'),
        ('rayskie', 'Yangi dizayn trendlari haqida o’ylab qoldim.', '2024-09-14 15:30:00'),
        ('yaxyo', 'Data Science va machine learning mavzusida ma’lumot yig’yapman.', '2024-09-14 16:00:00'),
        ('admin', 'Bugun serverda muammo paydo bo’ldi, hal qildik.', '2024-09-14 16:30:00'),
        ('rayskie', 'Frontend dizayn haqida yangiliklar topdim.', '2024-09-14 17:00:00'),
        ('yaxyo', 'Bugun vaqtni samarali o’tkazdim va ko’p narsalarni o’rgandim.', '2024-09-14 17:30:00');
    """)

    conn.commit()

    cur.close()
    conn.close()
