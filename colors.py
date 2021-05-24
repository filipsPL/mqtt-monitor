from datetime import datetime


class colors:
    '''
    Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold
    '''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'



class unicodeChar():
    class balls:
        green = '🟢 '
        orange = '🟠 '
        red = '🔴'
        yellow = '🟡 '
        blue = '🔵'
        brown = '🟤 '
        white = '⚪'
        purple = '🟣 '
        empty = '⭕️'
        noentry = '⛔'
    class squares:
        green = '🟩 '
        orange = '🟧 '
        red = '🟥 '
        yellow = '🟨 '
        purple = '🟪 '
        blue = '🟦 '



def pretty_date(time=False):
    """
    Based on https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    with some modifications
    """
    diff = datetime.now().timestamp() - time



    if diff < 86400:
        if diff < 10:
            return unicodeChar.balls.green + "just now"
        if diff < 60:
            return unicodeChar.squares.green +  str(round(diff)) + " seconds ago"
        if diff < 120:
            return unicodeChar.balls.blue +  "a minute ago"
        if diff < 3600:
            return unicodeChar.balls.yellow +  str(round(diff / 60)) + " minutes ago"
        if diff < 7200:
            return unicodeChar.balls.orange + "an hour ago"
        if diff < 86400:
            return unicodeChar.balls.red + str(round(diff / 3600)) + " hours ago"

    day_diff = diff / 86400

    if day_diff > 1 and day_diff < 1.5: # 1.5 days
        return unicodeChar.balls.empty + "Yesterday"
    if day_diff < 7:
        return unicodeChar.balls.noentry + str(round(day_diff)) + " days ago"
    if day_diff < 31:
        return unicodeChar.balls.noentry + str(round(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(round(day_diff / 30)) + " months ago"
    return unicodeChar.balls.noentry + str(round(day_diff / 365))    + " years ago"
