from colored import fg, attr

def __banner(color, text):
    print('{}[azurefire-infra]{} {}'.format(fg(color), fg('white'), text), flush=True)

def info(text):
    __banner('light_sky_blue_3a', text)

def error(text):
    __banner('red', fg('red') + attr('bold') + text + fg('white') + attr('reset'))

def success(text):
    __banner('light_green', text)
