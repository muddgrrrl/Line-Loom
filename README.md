# Line Loom

See whether a UTF-8 text file mixes Unix, Windows, or classic Mac line endings. Convert it when you need a consistent format.

```sh
python3 line_loom.py notes.txt
python3 line_loom.py notes.txt --to lf -o notes-clean.txt
```

Requires Python 3.8+. Conversion preserves the UTF-8 BOM and the presence or absence of a final line ending. The destination must be a new file. [MIT](LICENSE)
