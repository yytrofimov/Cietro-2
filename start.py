import sys
import os

sys.path.insert(0, './app/')

if __name__ == '__main__':
    import __init__

    __init__.app.run(host=os.environ.get('HOST'), debug=os.environ.get('DEBUG'), port=os.environ.get('PORT'))
