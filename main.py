import reader
import os


from pprint import pprint
from lexer import Lexer
from parser import Parser


def print_tokens(tokens):
  for token in tokens:
    if token['type'] == 'data':
      continue
    
    if token['type'] == 'start-tag':
      print('<%s>' % (token['name']))
      continue
    
    print('</%s>' % (token['name']))


def print_syntax_tree(syntax_tree, level): 
  indentation = '───' * level  

  for node in syntax_tree:
    if node['type'] == 'tag':
      
      attrs_string = ''
      
      if len(node['attrs']) > 0:
        attrs_string = node['attrs']
      
      print('%s %s  %s' % (indentation, node['name'], attrs_string))
    
    elif node['type'] == 'data':
      print('%s %s' % (indentation, node['data']))
      
    print_syntax_tree(node['children'], level + 1)


data = reader.read('./entry/index3.html')

lexer = Lexer(data)
tokens = lexer.parse()


parser = Parser(tokens)
syntax_tree = parser.get_syntax_tree()

if len(parser.errors) > 0:
  print('\n\nExecution error! There is one or more syntax errors in the source code\n\n')
  exit()

print_syntax_tree(syntax_tree, 0)