keyboard_dict = {
    "unauth": [['Registration📝', 'Library🏤', 'Search🔎', 'Help👤']],
    "unconf": [['Library🏤', 'Search🔎', 'Help👤']],
    "auth": [['Library🏤', 'Search🔎', 'My Books📚', 'Help👤']],
    "admin": [["Check material 📆", "Material management 📚", "User management 👥"]],
    "mat_management": [["Add material🗄", 'Library🏤', "Search🔎", 'Cancel⤵️']],
    "user_management": [["Confirm application📝", "Show users👥", 'Search user🔎', 'Cancel⤵️']],
    "reg_confirm": [["All is correct✅", "Something is incorrect❌"]],
    "lib_main": [['Books📖', 'Journal Articles📰', "Audio/Video materials📼", 'Cancel⤵️']],
    "cancel": [['Cancel⤵']],
    "status": [['Student', 'Faculty (professor, instructor, TA)']]

}

sample_messages = {
    'reg': """
        You have to provide your full name, address, phone number and status (student or faculty).\n
        Example:
        Ivan Ivanov,
        ul. Universitetskaya 1, 2-100,
        +71234567890,
        Student     
    """,

    'correctness': """
        Check whether all data is correct:
        Name: {name}
        Address: {address}
        Phone: {phone}
        Status: {status}
    """,

    'correctness_book': """
        Check whether all data is correct:
        Title: {title}
        Authors: {authors}
        Description: {description}
        Keywords: {keywords}
        Price: {price}
        Count: {count}
    """,

    'correctness_article': """
        Check whether all data is correct:
        Title: {title}
        Authors: {authors}
        Journal: {journal}
        Issue: {issue}
        Editors: {editors}
        Keywords: {keywords}
        Price: {price}
        Count: {count}
    """,

    'correctness_media': """
        Check whether all data is correct:
        Title: {title}
        Authors: {authors}
        Keywords: {keywords}
        Price: {price}
        Count: {count}
    """,

    'book': "You have to provide book's title, authors, overview, list of keywords, price (in rubles) and count.",

    'article': "You have to provide article's title, one or more authors, title of journal and its issue with editors and a\
        publication date. Also you need to provide list of keywords, price (in rubles).",

    'media': "You have to provide title, list of authors, list of keywords and price"
}

lists = {
    "user_types": ['unauth', "unconf", "auth", 'admin'],
    "reg_fields": ["name", 'phone', "address", "status"],
    'book': ['title', 'list of authors (divided by ";")', 'description', 'keywords (divided by ";")', 'price', 'count'],
    "article": ['title', ' list of authors (separated by ";")', 'journal title', 'issue', 'issue editors',
                'date of publication', 'keywords (separated by ";")', 'price', 'count'],
    "media": ['title', ' list of authors (separated by ";")', 'keywords (separated by ";")', 'price', 'count'],
    "book_bd": ['title', 'authors', 'description', 'keywords', 'price', 'count'],
    "article_bd": ['title', 'authors', 'journal', 'issue', 'editors', 'date', 'keywords', 'price', 'count'],
    "media_bd": ['title', 'authors', 'keywords', 'price', 'count'],
}

analog = {
    'Books📖': 'book',
    'Journal Articles📰': 'article',
    "Audio/Video materials📼": 'media'
}


def text_gen(data, location, page=0):
    sep = "\n" + "-" * 50 + "\n"
    text = [""]
    page = enumerate(data[page])
    if location in ['confirm', 'users']:
        text = ["{}) {} - {}".format(i + 1, item['name'], item["status"]) for i, item in page]
    if location == 'library':
        text = ["{}) {} - {}".format(i + 1, item['title'], item["authors"]) for i, item in page]
    if location == 'my_orders':
        text = ["{}) {}, till {}".format(i + 1, item['doc_dict']['title'], item["time_out"]) for i, item in page]
    if location == 'orders':
        page = enumerate(data)
        base = "{}) {} written by {}\n Available till {}"
        text = [base.format(i + 1, doc['doc_dict']['title'], doc['doc_dict']['authors'], doc['time_out']) for i, doc in page]
    return sep.join(text)
