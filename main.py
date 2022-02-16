from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote

db = sqlite3.connect("movies.sqlite")

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@get('/ping')
def ping():
    c = db.cursor()
    response.status = 200
    return "pong"

@post('/reset')
def reset_database():
    c = db.cursor()
    c.execute("DELETE FROM movie_theaters")
    db.commit()
    c.execute("DELETE FROM movies")
    db.commit()
    c.execute("DELETE FROM screenings")
    db.commit()
    c.execute("DELETE FROM tickets")
    db.commit()
    c.execute("DELETE FROM customers")
    db.commit()
    
    c.execute("""
    INSERT INTO movie_theaters(movie_theater_name, capacity)
    VALUES
    ("Kino", 10),
    ("Regal", 16),
    ("Skandia", 100)
    """) 
    db.commit()
    response.status = 201
    return {"data": "reset"}

@post('/users')
def post_user():
    user = request.json 
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO customers(customer_username, full_name, password)
            VALUES (?, ?, ?)
            """,
            [user['username'], user['fullName'], hash(user['pwd'])] 
                )
        db.commit()
        response.status = 201
        return f"/users/{user['username']}"
        
    except sqlite3.IntegrityError:
        response.status = 400
        return ""
        

@post('/movies')
def post_movie():
    movie = request.json 
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO movies(imdb_key, title, production_year)
            VALUES (?, ?, ?)
            """,
            [movie['imdbKey'], movie['title'], movie['year']] 
                )
        db.commit()
        response.status = 201
        return f"/movies/{movie['imdbKey']}"
        
    except sqlite3.IntegrityError:
        response.status = 400
        return ""


@post('/performances')
def post_performance():
    screening = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO screenings(imdb_key, movie_theater_name, screening_date, screening_time)
            VALUES (?, ?, ?, ?)
            RETURNING screening_id
            """,
            [screening['imdbKey'], screening['theater'], screening['date'], screening['time']]
                )
        screening_id = c.fetchone()        
        response.status = 201
        return f"/performances/{screening_id}"
    
    except sqlite3.IntegrityError:
        response.status = 400
        return "No such movie or theater"

@get('/movies')
def get_movie_search():
    query = """
        SELECT   imdb_key, title, production_year
        FROM     movies
        WHERE    1 = 1
        """
    params = []
    if request.query.title:
        query += " AND title = ?"
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND production_year >= ?"
        params.append(request.query.year)
    c = db.cursor()
    c.execute(query, params)
    found = [{"imdbKey":imdb_key,"title": title, "year":production_year} 
            for imdb_key, title, production_year in c]
    response.status = 200
    return {"data": found}




@get('/movies/<imdb_key>')
def get_students(imdb_key):
    c = db.cursor()
    c.execute(
          """
          SELECT  imdb_key, title, production_year
          FROM    movies
          WHERE   imdb_key = ?
          """,
          [imdb_key]
      )
    found = [{"imdbKey":imdb_key,"title": title, "year":production_year} 
            for imdb_key, title, production_year in c]
    response.status = 200
    return {"data": found}

@get('/performances')
def get_performances(): #TODO, Issue:"RemainingSeats", denna ger inte remainingSeats, utan returnerar bara capacity, se till så att den gör det den faktiskt ska
    c = db.cursor()
    c.execute( 
        """
        SELECT screening_id, screening_date, screening_time, title, production_year, movie_theater_name, capacity
        FROM screenings
        JOIN movies
        USING (imdb_key)
        JOIN movie_theaters
        USING (movie_theater_name)
        """
            )
    found = [{"performanceId": screening_id,"date": screening_date, "startTime":screening_time, "title": title, "year": production_year, "theater":movie_theater_name, "remainingSeats": capacity} 
            for screening_id, screening_date, screening_time, title, production_year, movie_theater_name, capacity in c]
    response.status = 200
    return {"data": found}

@post('/tickets')
def purchase_ticket(): #TODO, Issue: "PurchaseTickets", fixa så att man kan köpa tickets!
    pass
 
@get('/users/<username>/tickets')
def get_user_tickets(username): #TODO, Issue: "Se Users tickets", Just nu fungerar inte denna alls, se till så att denna fungerar och returnerar rätt
    c = db.cursor()
    c.execute(
        """
        SELECT
        FROM screenings
        JOIN customer
        USING (imdb_key)
        """
            )
    found = [{"performanceId": screening_id,"date": screening_date, "startTime":screening_time, "title": title, "year": production_year, "theater":movie_theater_name, "remainingSeats": capacity} 
            for screening_id, screening_date, screening_time, title, production_year, movie_theater_name, capacity in c]
    response.status = 200
    return {"data": found}


run(host='localhost', port=7007)

















































'''
@post('/users')
def post_user():
    user = request.json 
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO customers(customer_username, full_name, password)
        VALUES (?, ?, ?)
        """,
        [user['username'], user['fullName'], hash(user['pwd'])] 
            ) #TODO, Issue "Fixa post error handeling", om denna queryn crashar så kommer databasen ge error och kommer inte ge response.status = 400
    c.execute(
        """
        SELECT customer_username
        FROM customers
        WHERE rowid = last_insert_rowid()
        """
    )
    found = c.fetchone() 
    if not found: 
        #print("did not work")
        response.status = 400 
        return "Illegal..." #TODO, Issue: "Fixa post error handeling", ska inte vara illegal
    else:
        db.commit()
        #print("worked")
        response.status = 201
        username, = found
        return f"/users/{username}"
'''




'''
@post('/movies')
def post_movie():
    movie = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO movies(imdb_key, title, production_year)
        VALUES (?, ?, ?)
        """,
        [movie['imdbKey'], movie['title'], movie['year']]
            )
    #TODO, Issue: "Fixa post error handeling", borde bara crasha om det är duplicate keys, se till att den ger response.status = 400
    c.execute(
        """
        SELECT imdb_key
        FROM movies
        WHERE rowid = last_insert_rowid()
        """
    )
    found = c.fetchone() #TODO, Issue: "Fixa post error handeling", Om den har crashat så kommer den ändå kanske ge nåt här
    if not found: #TODO, Issue: "Fixa post error handeling", Tittar inte om den har get error eller inte
        #print("did not work")
        response.status = 400
        return "Illegal..."  #TODO, Issue:"Fixa post error handeling",  borde inte returnera "illegal"
    else:
        db.commit()
        #print("worked")
        response.status = 201
        username, = found
        return f"/movies/{username}"
'''