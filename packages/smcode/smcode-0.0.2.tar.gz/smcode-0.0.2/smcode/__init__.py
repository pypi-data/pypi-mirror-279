__all__ = ['selenium']

__version__ = '0.0.2'

from . import selenium

def is_latest_version() -> bool:
    """
    It checks if the current version of the package is the latest version
    :return: A boolean value.
    """
    import feedparser
    feed = feedparser.parse('https://pypi.org/rss/project/smcode/releases.xml')
    latest_version = feed.entries[0]['title']
    return __version__ == latest_version

def distinct(myList: list):
    """
    It takes a list as an argument, converts it to a dictionary, and then returns the list of keys
    
    :param myList: list
    :type myList: list
    :return: A list of unique values from the list passed in.
    """
    return list(dict.fromkeys(myList))

def update_smcode() -> None:
    """
    It updates the PATH environment variable to include the Python 3.4 and 3.8 directories, then runs
    the command `python -m pip install -U smcode` to update the `smcode` package
    """
    import os
    import subprocess
    os.environ['PATH'] = ';'.join(distinct(os.getenv('PATH').split(';') if os.getenv('PATH') else [] + ["C:\\Python38\\Scripts\\", "C:\\Python38\\", "C:\\Python34\\Scripts\\", "C:\\Python34\\"]))
    subprocess.run(['python', '-m', 'pip', 'install', '-U', 'smcode'], stdout=subprocess.DEVNULL)

def refresh() -> None:
    """
    It reloads the current module
    """
    import sys
    import importlib
    importlib.reload(sys.modules[__name__])


try:
    is_outdated = not is_latest_version()
except Exception as e:
    try:
        import os, ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
            is_outdated = not is_latest_version()
            
    except Exception as e:
        import warnings
        warnings.warn(f"{type(e).__name__}: Skipped auto update sequence because error occurred while checking the version", Warning)
else:
    if is_outdated:

        try:
            update_smcode()
        except Exception as e:
            import warnings
            warnings.warn(f"{type(e).__name__}: Skipped auto update sequence because error occurred while updating", Warning)
        else:
            refresh()
