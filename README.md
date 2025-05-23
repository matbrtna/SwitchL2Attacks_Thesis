# metelTest

Tato aplikace slouží k automatickému výkonnostímu a penetračnímu testování přepínačů společnosti METEL s.r.o.

## Instalace

Pro instalaci projektu spusťte BASH skript s názvem 'install.sh'. Po spuštění budou stáhnuty potřebné programy, které aplikace využívá a sestaví se binární soubor.

## Použití

Pro spuštění nainstalovaného projektu stačí do CLI zadat "metelTest" a následně přidat případné parametry:

-t	Spustí test omezení rychlosti. Je potřeba zadat parametr (např. -t 50 pro omezení na 50 Mbps).
-l	Spustí test rychlosti opravy topologie (např. při změně cesty v síti).
-m	Spustí útok MAC flooding (využívá nástroj macof).
-r	Spustí útok na RSTP pomocí falešných BPDU rámců.
-k	Ukončí procesy tcpdump a macof, pokud nebyly ukončeny správně.
-h	Zobrazí tuto nápovědu.

## Struktura projektu

.
├── test_configs/
├── test_results/
├── unit_tests/ 
│
├── build_metelTest.py
├── config.json
│
├── connectionLossAnalysys.py
├── connectionSpeed.py 
├── connectionThrottling.py
├── fTester.py 
│
├── install.sh
├── macFlooding.py
├── main.py
├── metelTest.spec
│
├── processes.py
├── processKill.py
│
├── rstpAttack.py
├── scapyPackets.py
│
├── setup.py
├── utils.py 
├── vlanTest.py
