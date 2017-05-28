from colored import fg, attr

def __banner(color, text, *args, **kwargs):
    if args or kwargs:
        message = text.format(*args, **kwargs)
    else:
        message = text

    print('{}[azurefire-infra]{} {}'.format(fg(color), fg('white'), message), flush=True)

def info(text, *args, **kwargs):
    __banner('light_sky_blue_3a', text, *args, **kwargs)

def error(text, *args, **kwargs):
    __banner('red', fg('red') + attr('bold') + text + fg('white') + attr('reset'), *args, **kwargs)

def success(text, *args, **kwargs):
    __banner('light_green', text, *args, **kwargs)
