# Projekti aruanne

## Projekti kirjeldus
Projekti eesmärk oli välja selgitada, kas isikukoodi kirjutamisel on võimalikke juhuslikke eksimusi rohkem siis kui kasutada praegust Eesti isikukoodi kontrollnumbri arvutamise valemit (https://et.wikipedia.org/wiki/Isikukood) või siis kui kasutada Luhni algoritmi (https://en.wikipedia.org/wiki/Luhn_algorithm).

Eksimust loetakse juhuslikuks kui kasutaja sisestab klaviatuurilt isikukoodi ühes numbris õigest numbrist kas ühe võrra suurema või väiksema numbri nii, et isikukoodi kontrollnumber on endiselt sama. S.t et kontrollnumber ei taga juhusliku eksimuse esinemist isikukoodi sisestamisel (sama kehtib ka pangakaartide, kontonumbrite jpms korral).

## Ülevaadet tööprotsessist
Projekti eesmärgi saavutamiseks on mõistlik kasutajalt küsida isikukoodide vahemikku, sest kõigi teadaolevate isikukoodide läbikontroll võib võtta ebamõistlikult kaua aega.

Isikukoodide kontrollimisel veendutakse isikukoodi tehnilises korrektsuses (funktsioon is_id_valid, milline omakorda kasutab funktsioone is_id_len, is_id_digit, is_id_century, is_id_date, is_id_check) ning seejärel leitakse funktsiooni find_similar abil kõik selle isikukoodiga sarnased (võimalikud juhuslikud eksimused). Sarnasuse leidmiseks genereeritakse igast isikukoodist vähemalt 20 uut koodi (vähendades ja suurendades isikukoodi esimesest kümnest numbrist igaüht ühe võrra), leitakse nende kontrolljärk ja võrreldakse algse isikukoodi kontrolljärguga. Kontrolljärkude võrdsuse korral loetakse uus isikukood sarnaseks algsega.

Sarnasusi otsitakse kasutades nii Eesti isikukoodi kontrolljärgu leidmise algoritmi kui ka Luhni algoritmi.

### Ülevaade ajakulust

Programmi struktuurile ja vajadustele olen mõelnud umbes 4 nädalat. Valminud on see jupikaupa vastavalt õpikõverale.
Esmased versioonid olid lihtsad ja ilma lisaarvutuste ning veaotsinguteta. 
Enim aega, kokku umbes 8h kulus 20-21.mail 2017 selleks, et esitada see kursusele LTAT.TK.001 piisavalt kommenteeritud ja silutuna.

Kokku kulus aega suurusjärk 16h.

### Hinnang oma töö lõpptulemusele

Arvan, et sain hästi hakkama ülesandest olulisega.
Töö tegemise käigus otsisin lisamaterjale internetist (python dokumentatsioon, stackoverflow jpt).
Kõik internetist leitud lisamaterjalid on kommenteeritud viitega (funktsioonid is_date_valid, Luhni algoritm, sanitised_input, query_yes_no, group)

Programmis on kasutusel:
- tsükkel,
- valikulause,
- funktsioon,
- failist lugemine või faili kirjutamine,
- järjend,
- lihtne graafika või graafiline kasutajaliides (EasyGUI).

Veel tegemist ja täiendamist vajavad kohad on programmi lähtekoodis varustatud märgenditega TODO.

### Selgitust ja/või näited, kuidas programmi osi eraldi ja programmi tervikuna testisin

Erinevad testid on toodud ja kommenteeritud programmi koodis. Kogu kood ja kommentaarid ja vaheväljatrükid on ingliskeelsed.

- For test purposes, some unit tests, is_id_valid(id)
- For test purposes, few similar known pairs
- For test purposes

Programmi töö silumiseks kasutasin ka globaalset keskkonnamuutujat debug, mille väärtusest sõltub vaheväljatrükkide arv.
Muutuja debug = 3 korral kasutatakse vaheväljatrükkides EasyGUI graafikat.
