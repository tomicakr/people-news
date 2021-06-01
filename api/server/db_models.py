def to_post(db_object):
    return {
        'url': db_object['url'],
        'title': db_object['title'],
        'text': db_object['text'],
        'hash': db_object['hash'],
    }
