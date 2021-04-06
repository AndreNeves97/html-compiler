
from html.parser import HTMLParser



class Lexer:
  def __init__(self, source):
    self.source = source

  def parse(self):
    parser = MyHTMLParser()
    parser.feed(self.source)
    return parser.tokens

    
    
    

class MyHTMLParser(HTMLParser):
  tokens = []

  def handle_starttag(self, tag, attrs):
    self.tokens.append({
      'type': 'start-tag',
      'name': tag,
      'attrs': attrs
    })
    

  def handle_endtag(self, tag):
    self.tokens.append({
      'type': 'end-tag',
      'name': tag
    })

  def handle_data(self, data):
    data = data.strip()
    
    if data == '':
      return
    
    self.tokens.append({
      'type': 'data',
      'data': data
    })
