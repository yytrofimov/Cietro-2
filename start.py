import sys

sys.path.insert(0, './app/')

if __name__ == '__main__':
    import __init__

    __init__.app.run(debug=True)
