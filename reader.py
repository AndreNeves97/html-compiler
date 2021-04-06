import sys

def read(file):
  
  try:
    file = open(file)
    data = ''

    with file:
      data = file.read()

    return data  
  
  except IOError as e:
    print('Erro de "IO" ao ler o arquivo: \n\n')
    print(e)
    print('\n\n')
    sys.exit()
  except:
    print('Erro desconhedo ao ler o arquivo: \n\n')
    print(sys.exc_info())
    print('\n\n')
    sys.exit()
      