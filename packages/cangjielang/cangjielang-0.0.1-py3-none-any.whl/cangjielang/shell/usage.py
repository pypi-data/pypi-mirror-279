from time import ctime

from cangjielang import __version__


def run():
    cur_time = ctime()
    text = f"""
    # cangjielang
    
    version {__version__} ({cur_time} +0800)
    """
    print(text)
