
Skrypty przerabiają pliki stylów .mapx, zmieniając im m.in. kolory.

<li>mapx_na_czarno_bialo.py - zmienia wszystkie kolory w mapxie dla wybranego modelu barw (parametr colorModel) na skalę szarości poprzez uśrednienie</li>
<li>mapx_zmiana_na_podstawie_sciezki.py - dla wybranego modelu barw i lokalizacji w mapx zmienia kolory na wskazane</li>
<li>wyswietlanie.py - tworzy tabelę w csv, zawierającą lokalizacje w podanym mapxie dla wszystkich znalezionych kolorów. Na podstawie tej tabeli, a dokładniej wartości uzupełnionych w trzech pierwszych jej kolumnach oraz ścieżki w mapx, zmieniane są kolory przy użyciu kolejnego skryptu </li>
<b>Po wygenerowaniu pliku CSV należy wpisać nowe wartości RGB (3 pierwsze kolumny) dla wierszy z lokalizacją mapx, dla której chcemy zmienić kolor. Plik ten musi być zapisany w kodowaniu utf-8</b>
<li>zczytywanieIZmienianie.py - na podstawie wartości w pliku csv zmienia wybrane kolory w mapxie dla lokalizacji odpowiedniej dla wiersza gdzie wypełnione zostały co najmniej wartości w trzech pierwszych kolumnach</li>
Przykładowe parametry:

```python
colorModel = r"CIM.*Color" # wszystkie modele barw
colorModel = r"CIMRGBColor" # tylko RGB
pathParameters = ['layerDefinitions', 'renderer', 'symbol', 421] # ścieżka w mapxie podana jako lista nazwy węzłów i/lub numery elementów
colorValues = [212, 515, 505, 0] # wartości na jakie chcemy zmienić, podane w wybranym modelu barw
```