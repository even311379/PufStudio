from pygments.formatters import HtmlFormatter
from pygments import styles

def GenStyle():
    sl = []
    for i, s in enumerate(styles.get_all_styles()):
        print(f'{i}:    {s}')
        sl.append(s)
    CodeStyle = sl[int(input('choose which style?'))]
    with open('blog/static/css/pygments.css', 'w') as f:
        f.write(HtmlFormatter(style=CodeStyle).get_style_defs('.codehilite'))
    print('Done! Successfully Write file to blog/static/css/pygments.css')


if __name__ == '__main__':
    GenStyle()

