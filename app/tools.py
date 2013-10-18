def composeDB(params):
    if params['DB_USER']:
        user = ':'.join((params['DB_USER'],params['DB_USER']))
    else:
        user = ''
    url = "mongodb://%s@%s:%s/%s" % (user, params['DB_HOST'], params['DB_PORT'], params['DB_NAME'])

    return url