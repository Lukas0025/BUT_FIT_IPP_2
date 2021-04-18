Implementační dokumentace k 2. úloze do IPP 2020/2021
Jméno a příjmení: Lukáš Plevač
Login: xpleva07

## Popis

Projekt 2. obsahuje dva seperátní skripty. První je interpret (v Python3) jazyka IPP21 reprezentovaný XML kódem vytvořeným 1. projektem. Druhý je script (v PHP7.4) pro provedení testů pro projekt 1.  a projekt 2. a vygenerování souhrnu výsledků testů v HTML na STDOUT.

## Soubory projektu

* errors.py - obsahuje funkce pro ukončení programu se specifickým return codem
* inscructions.py - obsahuje instrukce jazyka IPP21 a jejich interpreteci pro jazyk Python3
* interpret.py - hlavní soubor projektu obsahuje parse argumentů příkazů a následně volá interpret z ipp21.py
* ipp21.py - Soubor obsahuje inmplementaci interpretu IPP21 a includuje si inscructions.py
* program_file.py - obsahuje kód pro zpracování XML reprezantace kódu
* symtable.py - obashuje implementaci tabulky symbolů

* html.php - obahuje funkce pro generování HTML kódu
* test_support.php - obsahuje funkce pro provedení testů a kontrolu výstupů testů
* test.php - obashuje kontrolu argumentů příkazu, spustění testů a generování HTML pomocí pomocních PHP souborů

## Tabulky symbolů

je implementována v souboru symtable.py. Obsahuje zásobník rámců, přičemž po vytvoření již v zásobníku existuje jeden frame který reprezentuje `GF`, dále obsahuje tabulku pro `labels` a proměnou pro `TF`. `frame` je objekt instace třídy `frame` který obsahuje metody pro deklaraci proměnné, přiřazení hodnoty do proměnné a získání kodnoty proměnné, přečemž když se nějaká z těchto operací nazdaří (proměnná neexistuje, není inicializována, ...) metoda ukončí interpret se specifickou chybou a podrobnosti vypíše na `STDERR`. Práce s lokálním rámecem `LF` je implemenaváná stejně jako s globálním (`LF`, `GF` a `TF` jsou instance stejné třídy), přičemž `LF` je chpán jako `frame_stack[-1]` za podmínky `len(frame_stack) > 1`.  Při volání `CREATEFRAME` bude vytvořena nová instance třídy frame a odkaz na ní bude uložen do tabulky. Při volání `PUSHFRAME` bude tento odkaz vložen za zásobník  `frame_stack`. Při volání `POPFRAME` bude vyjmut poslední `frame` z zásobníku a odkaz bude vložen do proměnné pro `TF`. `Labels` jsou řešeny mimo rámce přímo v tabulce, jsou zde metody pro vytvoření `label` a zjištení adresy `label`, při chybě bude vyvoláno ukončení programu se specifickou chybou. Tabuka symbolů obsahuje také funkce na zjištění datového typu a hodnoty libovolného výrazu jako je např `GF@test` ale i `string@hello`, při chybě opět ukončuje program se specifickou chybou.

## Interpret jazyka IPP21

TOP soubor implementace je `ipp21.py`. Poté co je soubor programu nasčten a instrukce jsou seřazeny podle `order` metodamy v `program_file.py`  je program zpracován interpretem. Všechny instrukce jsou nejříve přečteny a nejsou interpretovany s vyjímkou instrukce `LABEL` ta je jako jediá provedena. Následně se program spustí opetět od instrukce 0, ale nyný budou igoravány instrukce `LABEL`. instrukce je vždy přečtena a pomocí metody v `inscructions.py` je přeložena na adresu funkce interpretující danou instrukci (pokud překlad selhal, je přeložena na adresu funkce která unkončí interpret s chybou). Na začátku každé takové funkce je kontrola datových typů argumetů, které jsou kontrolovány pomocí speciální metody v `inscructions.py`. Tato metoda se dotáže Tabulky symbolů na datavý typ argumentu a následně se ptá zda je `IN` array očekávaných typů, pokud není ukončí interpret s chybou. Poté následu kód specifický pro instrukci a na konci je inkrementace `IP` (instruction pointer) s vyjímkou instrukcí skoku, zde se k `IP` chová jinak. Interpret takto pokračuje dokud `IP` nebude větší/roven počtu instrukcí v programu, poté se ukončí.

## Testovací rámec (test.php)

Provádí testování skriptů projektu prvního a druhé. výstup zobrazuje jako HTML stránku. Pokud všechny argumenty sedí a cesty k souborů a složkám jsou dostupné ke čtení spustí testy jinak skončí s chybou. Testy hledá pomocí `GLOB` jako `*.src` pokud najde spustí test a nsáledně pomocí `DIFF` zkontroluje návratový kód který se uloží do souboru *.testrc pokud odpovídá kóu v `*.rc` a je roven 0 tak ještě zkontroluje zda odpovídá `*.testout` a `*.out` (kontroluje pomocí `DIFF` nebo `jexamxml` zaáleží zda se testuje parser nebo interpret) pokud ano vydonotí že test prošel jinak hodnotí že neprošel. Soubory `*.test*` neodstranujě, aby bylo po testu možné zjiastit proč test neprošel. ty výsledky je nutné po testu odstranit ručně pomocí `rm -f *.testout && rm -f *.testrc`.

## Makefile

* zip - vytvoří zip archv pro odevzdání
* jexamxml - stráhne jexamxml z internetu
* test-dir - votvoří testovací složku které obasuhuje soubory zip archybu pro odevzdání
* test - spustí testy pro interpret
* clean - vyčistí lokální adresář projektu

## Rozšíření
* Nedokončené FLOAT (bez podpory načtení se specifickým formátem)
