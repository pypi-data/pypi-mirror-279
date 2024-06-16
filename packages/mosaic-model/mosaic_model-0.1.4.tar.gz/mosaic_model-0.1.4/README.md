<h1 align="center" id="title">Mosaic Model</h1>

<p id="description">Here I collected some online and offline models for text tagging.</p>

<h2>🚀 Demo</h2>

[All models usage](https://colab.research.google.com/drive/18HjmIi_4_g63GJwQgSNyTocxH_ZdqRya?usp=sharing)

<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Online model: Rake Based Model. 5-10 it/sec
*   Offline models: Bart based model with summarisation. 1-5 it/sec
*   API model: YandexGPT based model. 1-5 it/sec

<h2>🛠️ Installation Steps:</h2>

<p>1. Installation</p>

```
pip install mosaic-model
```

<p>2. import</p>

```
from mosaic-model.models.rake_based_model import TagsExtractor
```

<p>3. Init tagger</p>

```
tagger = TagsExtractor()
```

<p>4. Get tags</p>

```
tagger.extract(some_text)
```
