## Trywialny podział sektretu

Kiedy to podejście jest nie bezpieczne:

- mała wartość k wzgledem s - bardzo to zawęza zakres mozliwych wartości sektretu
- ujawnienie n-1 udziałow, kiedy znamy n-1 udziałów i wartość k to mozemy obliczyć brakującą cześć

Podstawowe wady tej metody:

- Brak progu (Threshold): Nie możesz ustawić zasady, że np. 3 z 5 udziałów wystarczy. W metodzie trywialnej zawsze muszą być wszytskie udziały ($n$ z $n$). Jeśli jeden udział przepadnie, sekret przepada na zawsze.
- Wrażliwość na modyfikacje: Metoda nie posiada mechanizmu weryfikacji. Jeśli jeden z uczestników poda błędny udział (celowo lub przez błąd transmisji), wynik sumowania będzie błędny, a Ty nie będziesz wiedział, kto zawinił.
- Zależność od $k$: W Twoim kodzie musisz bezpiecznie przechowywać lub przekazać również wartość $k$. Jeśli uczestnicy znają udziały, ale zapomną, jakie było $k$, nie odtworzą sekretu poprawnie.

## Podział sekretu Shamira

Jaka jest minimalna liczba udziałów aby algorytm działał poprawnie?

k=2 to minimum, trzeba mieć co najmniej 2 udziały, żeby odzyskać sekret

- pojedynczy udział nic nie ujawnia
- to najprostsza wersja, która faktycznie realizuje ideę „secret sharing”
