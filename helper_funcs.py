from datetime import datetime


def shortenStringToFit(input_string, max_length, mode=0):
    if mode == 0:
        if len(input_string) < max_length:
            result = "Log file: " + input_string
        else:
            result = "Log file: ..." + input_string[(-1 * max_length):]
    elif mode == 1:
        if len(input_string) < max_length:
            return input_string
        else:
            result = input_string[0:6]+"..."+input_string[(-1*max_length-9):]

    return result


def timeNowString():
    return str(datetime.now().strftime("%-m/%-d/%Y [%-I:%M %p]")).lower()

