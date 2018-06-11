def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

# def create_book(conn, book):
def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def main():
    database = "/db.sqlite3"
    import os
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    application = get_wsgi_application()
    import csv
    from books.models import Book
    from django.contrib.auth.models import User

    reader = []

    with open("books_list.csv") as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')

        for line in reader:
            try:
                user = User.objects.get(id=line['auth_user'])
                book = Book(title=line['title'], image_url=line['image_url'], author=line['author'], publisher=line['publisher'], category=line['category'], user=user)

                book.save()
            except:
                continue

        # print(line["last_name"])

    #
    # if __name__ == "__main__":
    #     with open("data.csv") as f_obj:
    #         csv_dict_reader(f_obj)

    # create a database connection

if __name__ == '__main__':
    main()

