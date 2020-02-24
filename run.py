# -*- coding: utf-8 -*-


from api import app
from scheduler import Schedule


def main():
    s = Schedule()
    s.run()
    app.run()


if __name__ == '__main__':
    main()