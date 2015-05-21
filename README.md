# Demoteilnehmer-Counter

## Zählt Menschen im Videobild

![Demo](https://raw.githubusercontent.com/balzer82/Demoteilnehmer-Counter/master/screenshots/pegida_demo_11052015_043_marked.jpg)

Klappt fast perfekt, wenn die einzelnen Menschen im Ganzen zu sehen sind (also incl. Beinen). Weil das bei Demos fast nie so ist, gibt es einen `crowd_factor` der das Verdecken ausgleicht. Umso dichter die Menschen stehen, umso höher muss dieser sein.

### Beispiel: SCHÄTZUNG TEILNEHMERZAHL PEGIDA 11.05.2015

Inspiriert durch [STUDENTENGRUPPE "DURCHGEZAEHLT"](https://durchgezaehlt.wordpress.com/2015/05/12/schatzung-teilnehmerzahl-pegida-11-05-2015/) mit deren Video von der Pegida Demo vom 11.05.2015 in Dresden.

![](http://i.imgur.com/aW8KocQ.jpg)

### [Für Code: IPython Notebook ansehen](https://github.com/balzer82/Demoteilnehmer-Counter/blob/master/videocounter.ipynb)

## Wie gut klappt das automatisch?

```
automatisch: 2.600 Teilnehmer
vom Menschen: 2.597 Teilnehmer (durch STUDENTENGRUPPE "DURCHGEZAEHLT")
```

## Wie lange dauert das?

Ungefähr 10min incl. Video runterladen, in Einzelbilder verwandeln und durch OpenCV jagen.


## Wie geht das?

1. Python
2. OpenCV
3. Histogram of oriented gradients (HOG) Descriptor
4. ffmpeg

