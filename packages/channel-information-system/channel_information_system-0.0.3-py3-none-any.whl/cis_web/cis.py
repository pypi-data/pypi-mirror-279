from flask import Flask
from ja_webutils.Page import Page
from ja_webutils.PageItem import PageItemHeader, PageItemLink

app = Flask(__name__)


@app.route('/')
def cis():  # put application's code here
    page = Page()
    page.title = 'Channel Information System'
    page.add(PageItemHeader('Welcome to the future home of the IGWN Channel Information System'))
    page.add_line('The original CIS has been determined to be a security risk  because it has not been updated in so '\
                  'long.',0, 2)
    page.add_line('Data from the previous version is avalable as a  ', 0, 0)
    ss = PageItemLink('https://docs.google.com/spreadsheets/d/1ZeSHQGeAiFsSYE4X9LFvSNqzQmzZB02YyGpT-0Vj6AE/edit?usp'
                      '=sharing', 'google spreadsheet')
    page.add(ss)

    page.add_line('Feel free to add to the spreadsheet, all data from the spreadsheet will be added to '
                  'new CIS before release', 2, 2)
    html = page.get_html()
    return html

if __name__ == '__main__':
    app.run()