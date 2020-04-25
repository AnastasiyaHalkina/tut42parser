from staticjinja import Site
from tut42_parser import main
import datetime


def get_date():
    cur_date = datetime.datetime.now()
    return cur_date.strftime('%d/%m/%Y')


if __name__ == "__main__":
    context = {'articles': main()}
    current_date = {'now': get_date()}
    site = Site.make_site(contexts=[('index.html', context), ('index.html', current_date)], mergecontexts=True,)
    site.render(use_reloader=True)
