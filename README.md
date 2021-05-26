# HTML syntactic analyzer

Analisador sintático básico para `HTML`, desenvolvido em Python.

O analisador sintático tem a função de receber a lista de tokens (objetos da linguagem), com o objetivo de verificar e gerar a árvore da estrutura sintática do código.

Uma das verificações realizadas pelo analisador sintático é avaliar o correto fechamento de de escopos abertos por parênteses, colchetes e chaves.

Esse projeto utiliza a bibliioteca `HTMLParser` para análise léxica e parsing dos tokens do código `html`. A partir da obtenção da lista de tokens, é feita a análise sintática e geração da árvore de elementos.

## Bibliotecas utilizadas:

- 'os'
- 'sys'
- 're'
- 'pprint'
- 'HTMLParser'


## Execução:

```bash
## Executar o script de entrada
python3 main.py
```

Os códigos de teste utilizados então em `./entry`. O ponto de entrada `main.py` é responsável pela leitura do arquivo `index.html`, seguido do processamento do conteúdo.


## Demonstração

O seguinte código foi utilizado para o teste base:

```html
<html>
  <head>
  </head>
  <body>
    <p>Teste</p>
    <h1>asdasd</h1>
    

    <social-icons *ng-if="teste" class="social">
      <div>
        <a href="google.com" class="teste"></a>
      </div>
    </social-icons>

    <div>Final content</div>
  </body>
</html>
```

Resultado do analisador sintático:

```bash
─── head  
─── body  
────── p  
───────── Teste
────── h1  
───────── asdasd
────── social-icons  [('*ng-if', 'teste'), ('class', 'social')]
───────── div  
──────────── a  [('href', 'google.com'), ('class', 'teste')]
────── div  
───────── Final content

```


Esse caso de teste não possui um código com erros. Os arquivos `entry/index2.html` e `entry/index3.html` possuem exemplos com erros sintáticos do html, como:


- Outra tag diferente de `<html>` na raiz do documento
- Outras tags diferentes de `<head>` e `<body>` dentro de `<html>`
- Tags `<head>` e `<body>` fora da tag `<html>`
- Tag `<li>` fora da tags `<ul>` ou `<ol>`
- Repetição das tags `<html>` e `<body>`
- Tag aberta sem fechamento
- Fechamento incorreto de tag



### Código com erro

```html
teste

<!-- </div> -->


<p>
  <b>
</p></b>
  
<!-- <b> -->


teste

<head>
  tste
</head>


<html>
  <div class="row col">
    <h1>título</h1>
    <h2>subtítulo</h2>
    teste andre
    neves
    <img src="" alt="" />
  </div>

  <div>
    <h1>título 2</h1>
    <h2>subtítulo 2</h2>
  </div>

  <social-icons *ng-if="teste" class="social">
    <div>
      <a href="google.com" class="teste"></a>
    </div>
  </social-icons>
</html> 
```

Saída obtida:

```
Syntax error! Mismatch tag <p> inside root. Only <html> should be placed inside root

Syntax error! Found close tag </p>. Expected: </b>

Syntax error! Wrong place for tag <head> (Inside <p>). Should be inside ['html']

Syntax error! Mismatch tag <div> inside <html>. Only <head> or <body> should be placed inside <html>

Syntax error! Mismatch tag <div> inside <html>. Only <head> or <body> should be placed inside <html>

Syntax error! Mismatch tag <social-icons> inside <html>. Only <head> or <body> should be placed inside <html>

Syntax error! Close tag <\p> expected


Execution error! There is one or more syntax errors in the source code
```