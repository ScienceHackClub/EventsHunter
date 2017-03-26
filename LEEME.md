
## Este programa:

1. Extrae rss y feeds configurados en config.json

2. Preprocesa los datos extraídos (modules/regex_data.py)
  2.1. Limpia html, elimina excesos de espacios, etc
  2.2. Sustituye links, fechas, horas, etcétera por TAGS para facilitar
  el posterior procesado por NLTK.

3. Extrae datos específicos a partir del motor de NLTK (modules/nltk_parse.py).


## Debug
Si activas debug=1, no se conectará a internet y usará los datos de
./debug/??.pickle


## Entrenar el dataset

- La red entrenada se encuentra archivos pickle en la carpeta ./data

- El dataset se encuentra en ./train.

- Hay dos variantes de dataset (rss y twitter). La diferencia está en que
los rss traen ya el título del post explícito, pero los twits no, por lo
que kener-twitter.train INCLUYE named entities de tipo "MAIN". Lo que esto
extraiga luego servirá de título.

- ¿Cómo lo entreno?
  1 - Instalar nltk y nltk_data

  2 - Configurar este archivo

    /usr/local/lib/python2.7/dist-packages/nltk/corpus/__init__.py

    y añadir esto:

    kenerator = LazyCorpusLoader(
    'kenerator', ConllChunkCorpusReader, '.*\.(test|train).*',
    ('LOC', 'PER', 'ORG', 'MISC', 'TIME', 'DATE', 'PRICE', 'MAIN'), encoding='utf-8')

    Lo que hará esto es decirle al entrenador que interprete los archivos
    .train igual que como los interpreta para el dataset de Conll2002.

  3 - Descargar nltk_trainer https://github.com/japerk/nltk-trainer

  4- Meter UN SOLO archivo .train (twitter o rss) en una nueva carpeta
  llamada kenerator en la carpeta donde está instalado nltk_data

  5- Entrenar los archivos CHUNKER y TAGGER. El tagger pone etiquetas
  POS (verbos, adjetivos, adverbios, nombres...) a palabras que sirven para generalizar los datos y que el chunker pueda relacionar datos desconocidos.

  python ./train_tagger.py kenerator --filename kener-twitter-tagger

  python ./train_chunker.py kenerator --classifier NaiveBayes --filename kener-twitter-chunker


- ¿por qué "kenerator"? porque NER es acrónimo de named-entity recognition,
y ya que mi apellido es keNER, pues...


## FAQ

- ¿Por qué funciona como el culo?:

  Es normal si te dice que la fecha del evento es "tortilla de papas", necesitamos múltiple mano de obra barata para que hagan un buen pedazo
  de .train (y específico para lo nuestro, por eso no cogí el dataset de CESS_ESP ni el CONLL2002 que incluye nltk_data)


## BUGS

- Está poco testada la forma de restaurar los tags en los named entities
devueltos. Seguro que la lía a veces

- No consigo quitar los &amp;quotes;, comillas y demás mierdas raras

- Los POS-tags (part-of-speech tags) que puse, tipo (VSA, NC, NP, ADL...)
probablemente no son los óptimos para el sistema, habrá que indagar en esto
