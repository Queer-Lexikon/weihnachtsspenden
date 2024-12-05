# Das Postkartenaktionsdingsi

Wir wollen:
- ermöglichen Spenden zu Weihnachen zu verschenken
- Spenden dabei direkt über Lastschrift einziehen

das passiert so:
- es gibt eine statische Landingpage
- es gibt ein sehr schlankes Backend, das Daten entgegen nimmt
- das Backend legt die jeweils als JSON ab
- das Backend ist fastapi, was über Pydantic Types und Safety produziert

## Setup

Das sollte prinzipiell etwa so gehen

- venv generieren (wir wollen Python 3.11 oder neuer)
- `pip install -r requirements.txt`
- schnell im WordPress checken, wie viele Fördermitgliedschaften schon da sind und gegebenenfalls die `+34` in der `get_current()` anpassen
- mit `fastapi run main.py --port ABC` mit einem freien Port für ABC starten und das Reverse-Proxy dran kleben

optional: in der Theorie kann, was im `static/` liegt, auch am ASGI vorbei geserved werden.

## Customize

Das leider bisschen murky, aber:

- Wer **Texte** anpassen mag, findet die alle in der `static/index.html`. Alles, was HTML kann, ist prinzipiell möglich, es wird nichts gefiltert oder geprüft.
- Wer **Design** anpassen mag, wird in `static/generic.css` fündig. Das deklariert oben eine Menge Variablen, so dass abtauchen zu spezifischen Klassen oft gar nicht mehr dringend ist.

## was ist noch?

- vor dem abschicken die formData checken, dass alles notwendig da ist (zeile 373)
  - gegebenenfalls nicht stimmige Dinge highlighten und hinscrollen
- nach dem abschicken die Antwort anschauen (Zeile 406)
  - die sollten immer erfolgreich sein, wenn es clientseitig gepasst hat, außer
  - wenns den Eintrag schon gibt
  - oder wenn die IBAN nicht valide ist
  - auch das aufzeigen
- einge schöne Erfolgsmeldung fehlt noch (ungefähr Zeile 404)