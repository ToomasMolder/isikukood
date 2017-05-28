# Projekti aruanne

## Projekti kirjeldus

Projekti eesmärk oli tekitada esialgsed meetodid Eesti isikukoodi korrektsuse kontrolliks, kontrollnumbri leidmiseks ning selgitada välja, kui palju on võimalikke juhuslikke eksimusi (sarnasusi) konkreetse isikukoodi kirjutamisel.

Eksimust loetakse juhuslikuks (isikukoodid sarnasteks) kui need on korrektsed, sama kontrollnumbriga kuid erinevad üksteisest vaid ühe sümboli osas ühe numbri võrra (algsest suurem või väiksem). Juhuslike eksimuste võimalikkuse korral ei taga kontrollnumber isikukoodi korrektsust.

Projekti eesmärgi tuletasin 05.04.2017 Eesti Päevalehe artiklist "e-põrgu kadalipp: kuidas tõestada, et sa pole skisofreeniahaige" (http://epl.delfi.ee/news/eesti/e-porgu-kadalipp-kuidas-toestada-et-sa-pole-skisofreeniahaige?id=77783596)

## Ülevaadet tööprotsessist

Projekti eesmärkide saavutamiseks realiseerisin algsed isikukoodi kontrollnumbri arvutamise ja korrektsuse kontrollid, need on koondatud funktsiooni is_id_valid, milline omakorda kasutab funktsioone is_id_len, is_id_digit, is_id_century, is_id_date ja is_id_check.

Seejärel realiseerisin etteantud isikukoodi juhusliku eksimise otsimise funktsiooni find_similar_one(id, check), milline käib tsükliliselt mööda isikukoodi, muudab iga tema arvu (esimest kümmet arvu) ühe võrra suuremaks ja väiksemaks, arvutab muudetud isikukoodi uue kontrollnumbri ning juhul kui see on sama algse isikukoodi kontrollnumbriga, siis moodustab sõnastiku sarnastest, kus võtmeks on algne isikukood ning väärtuseks temaga sarnased (ühe numbri võrra erinevad kuid sama kontrollnumbriga).

Kõige lõpuks realiseerisin kasutajalt tema soovide küsimise osa funktsioonis what_to_do() ning lisasin sinna veel juhuslikult genereeritud isikukoodi ning kasutajalt saadud isikukoodide vahemiku juhuslike eksimuste otsimise funktsionaalsused.

Tööde käigus lisasin projektile võimalused valida tema töörežiim läbi globaalse muutuja os.environ['DEBUG'].

Tööde käigus restruktureerisin oluliselt algset lähtekoodi, viies korduvakasutatavad osad funktsioonideks, samuti jagasin loetavuse ning selguse huvides algse põhiprogrammi (main) osadeks sõltuvalt kasutaja valikutest ning lisasin tööks vajalikke internetiavarustest leitud elemente.

Enim tähelepanu pöörasin isikukoodide vahemikust juhuslike eksimuste leidmise sisenditele ja väljunditele, hindamiseks esitatud versioonis salvestatakse tulemused kettafaili, json-formaadis.

Tööde käigus katsetasin isikukoodi kontrollnumbri leidmist ning juhuslike eksimuste (sarnasuste) otsimist Luhni algoritmiga (https://en.wikipedia.org/wiki/Luhn_algorithm) kuid hindamiseks esitatud versioonis eemaldasin selle osa.

Programmi lähtekood, kommentaarid ja suhtlus kasutajaga on kirjutatud ingliskeelsetena, selleks, et vajadusel tulevikus kasutada eesti keelt mitte emakeelena kõnelevate arendajate abi.

### Ülevaade ajakulust

Programmi struktuurile ja vajadustele olen mõelnud ligi kaks kuud. Valminud on see jupikaupa vastavalt õpikõverale ja selleks võetud ajale.
Esmased versioonid olid lihtsad ja ilma lisaarvutuste ning veaotsinguteta. 
Kuna projekt valmis sõltumatult LTAT.TK.001 projektist, siis olen kokkuvõttes sellele kulutanud aega oluliselt rohkem kui minimaalselt nõutud 8 tundi.

### Hinnang oma töö lõpptulemusele

Arvan, et sain hästi hakkama ülesandest olulisega.
Töö tegemise käigus otsisin lisamaterjale internetist (python dokumentatsioon, stackoverflow jpt).
Kõik internetist leitud lisamaterjalid on kommenteeritud viitega (funktsioonid is_date_valid, Luhni algoritm, sanitised_input, query_yes_no, group jpm)

Programmis on kasutusel:
- tsükkel (for, while)
- valikulause (if, elif, else)
- funktsioon (def)
- faili kirjutamine (open, dump)
- järjend, ennik ja sõnastik ([], (), {})
- kahemõõtmeline andmestruktuur (funktsiooni inspect.stack() näitel; väljundis faili järjend sõnastikus)
- lihtne graafika või graafiline kasutajaliides (EasyGUI).

Veel tegemist ja täiendamist vajavad kohad on programmi lähtekoodis varustatud märgenditega TODO.

### Selgitust ja/või näited, kuidas programmi osi eraldi ja programmi tervikuna testisin

Programmi töö silumiseks kasutasin globaalset keskkonnamuutujat os.environ['DEBUG'], mille väärtusest sõltub vaheväljatrükkide arv.
Muutuja väärtuse 3 korral kasutatakse vaheväljatrükkides EasyGUI graafikat. EasyGUI tarbeks peab samas kaustas olema fail (saab kas http://easygui.sourceforge.net/või https://courses.cs.ut.ee/2017/eprogalused/spring/uploads/Main/easygui.py)

Programmi tööd on põhjalikult testitud järgmiste meetoditega:
- ühiktestid, kasutajalt saadud sisendi asemel alamprogrammidele otse muutujate etteandmisel (For test purposes, some unit tests, kommenteeritud programmi lähtekoodis)
- vaheväljatrükid, hiljem programmi lähtekoodist kas eemaldatud või välja kommenteeritud
- silumismuutuja os.environ['DEBUG'], väärtused 0 (error), 1 (warning) ja 2 (info)
- EasyGUI abil erinevate sisendite ja nupuklõpsudega

 
