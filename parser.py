class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.errors = []
    self.already_read_html = False
    self.already_read_body = False
    self.current_tag_token = None
    

  def get_syntax_tree(self):
    self.tree = []
    
    self.current_tag_token = None
    
    for token in self.tokens:
      token['children'] = []
      token['parent'] = None
      
      if token['type'] == 'data':
        self.handle_data(token)
        continue
      
      if token['type'] == 'start-tag':
        self.handle_start_tag(token);
        continue
      
      if token['type'] == 'end-tag':
        self.handle_end_tag(token)
        continue
      
    if self.current_tag_token != None:
      if self.tag_with_required_close(self.current_tag_token['name']):
        self.handle_close_tag_required_error(self.current_tag_token);

        self.tree.append(self.current_tag_token)
        self.current_tag_token = None

    return self.tree
  
  def handle_data(self, token):
    if self.current_tag_token == None:
      self.tree.append(token)
      return
    
    self.current_tag_token['children'].append(token)
  
  def handle_start_tag(self, token):
    token['type'] = 'tag'
  
    self.check_general_start_tag_errors(token, self.current_tag_token)

    if not self.tag_with_required_close(token['name']):
      if self.current_tag_token == None:
        self.tree.append(token)
        return
      
      self.current_tag_token['children'].append(token)
      return
      
    if self.current_tag_token != None:
      token['parent'] = self.current_tag_token
    
    self.current_tag_token = token
    
  
  def handle_end_tag(self, token):
    if not self.tag_with_required_close(token['name']):
      return
      
    if self.current_tag_token == None:
      self.handle_unexpected_close_tag_error(token)
      return
    
    
    if token['name'] == self.current_tag_token['name']:
      
      if self.current_tag_token['parent'] == None:
        self.tree.append(self.current_tag_token)
        self.current_tag_token = None
        return
      
      self.current_tag_token['parent']['children'].append(self.current_tag_token)
      
      next_tag = self.current_tag_token['parent']
      self.current_tag_token['parent'] = None
      
      self.current_tag_token = next_tag
      return
    
    
    self.handle_mismatch_close_tag_error(token, self.current_tag_token)
    
  
  
  def tag_with_required_close(self, tag_name):
    return tag_name not in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', 'command', 'keygen', 'menuitem']
  
  def check_general_start_tag_errors(self, token, parent_token):
    if token['name'] == 'html':
      if self.already_read_html:
        self.handle_repeated_tag_error(token)
      
      self.already_read_html = True
      
    if token['name'] == 'body':
      if self.already_read_body:
        self.handle_repeated_tag_error(token)
      
      self.already_read_body = True
    
    
    if token['name'] == 'li':
      if parent_token == None or (parent_token['name'] != 'ul' and parent_token['name'] != 'ol'):
        self.handle_wrong_place_for_tag_error(token, parent_token, ['ul', 'ol'])
    
    if token['name'] == 'head':
      if parent_token == None or (parent_token['name'] != 'html'):
        self.handle_wrong_place_for_tag_error(token, parent_token, ['html'])
    
    if token['name'] == 'body':
      if parent_token == None or (parent_token['name'] != 'html'):
        self.handle_wrong_place_for_tag_error(token, parent_token, ['html'])
    
    
    if parent_token == None:
      if token['name'] != 'html':
        self.handle_mismatch_tag_inside_root_error(token)
    else:
      if parent_token['name'] == 'html' and token['name'] != 'head' and token['name'] != 'body':
        self.handle_mismatch_tag_inside_html_error(token)

  
  def handle_wrong_place_for_tag_error(self, token, parent_token, required_parent_tags):
    if parent_token != None:
      print('Syntax error! Wrong place for tag <%s> (Inside <%s>). Should be inside %s' % (token['name'], parent_token['name'], required_parent_tags))
      
      self.errors.append({
        'type': 'WRONG_PLACE_FOR_TAG',
        'tag': token['name'],
        'parent_tag': parent_token['name']
      })
      
      return
    
    print('Syntax error! Wrong place for tag <%s>. Should be inside %s' % (token['name'], required_parent_tags))
    
    self.errors.append({
      'type': 'WRONG_PLACE_FOR_TAG',
      'tag': token['name']
    })
  
  
  def handle_mismatch_tag_inside_root_error(self, token):
    print('Syntax error! Mismatch tag <%s> inside root. Only <html> should be placed inside root' % (token['name']))
    
    self.errors.append({
      'type': 'MISMATCH_TAG_INSIDE_ROOT',
      'tag': token['name']
    })
    
  
  def handle_mismatch_tag_inside_html_error(self, token):
    print('Syntax error! Mismatch tag <%s> inside <html>. Only <head> or <body> should be placed inside <html>' % (token['name']))
    
    self.errors.append({
      'type': 'MISMATCH_TAG_INSIDE_HTML',
      'tag': token['name']
    })

  def handle_repeated_tag_error(self, token):
    print('Syntax error! Repeated tag <%s>' % (token['name']))
    
    self.errors.append({
      'type': 'REPEATED_TAG',
      'tag': token['name']
    })
  
  def handle_mismatch_close_tag_error(self, token, expected_token):
    print('Syntax error! Found close tag </%s>. Expected: </%s>' % 
          (
            token['name'], 
            expected_token['name']
          )
    )
    
    self.errors.append({
      'type': 'MISMATCH_CLOSE_TAG',
      'tag': token['name'],
      'expected_tag': expected_token['name']
    })
      
  def handle_close_tag_required_error(self, current_tag):
    print('Syntax error! Close tag <\%s> expected' % (current_tag['name']))
    self.errors.append({
      'type': 'CLOSE_TAG_REQUIRED',
      'tag': current_tag['name']
    })
      
  def handle_unexpected_close_tag_error(self, token):
    print('Syntax error! Found closing tag </%s> when it\'s not expected' % 
          (
            token['name']
          )
    )
    
    self.errors.append({
      'type': 'CLOSE_TAG_UNEXPECTED',
      'tag': token['name']
    })