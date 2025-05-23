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
├── test_configs/              # Konfigurační soubory pro jednotlivé testy
├── test_results/              # Stažené výsledky z F-Testerů pro testování aplikace
├── unit_tests/                # Jednotkové testy (např. pro connectionSpeed.py)
│
├── build_metelTest.py         # Sestavení prostředí nebo přizpůsobení testu
├── config.json                # Hlavní konfigurační soubor aplikace
│
├── connectionLossAnalysys.py  # Test výpadků spojení v síti
├── connectionSpeed.py         # Test maximální rychlosti v síti
├── connectionThrottling.py    # Test omezení propustnosti
├── fTester.py                 # Skript pro komunikaci s testery
│
├── install.sh                 # Skript pro instalaci závislostí a přípravu prostředí
├── macFlooding.py             # Útok MAC flooding 
├── main.py                    # Hlavní spouštěcí skript aplikace
├── metelTest.spec             # Konfigurační soubor pro pyinstaller
│
├── processes.py               # Skript pro spouštění podprocesů
├── processKill.py             # Nástroj na zabití běžících procesů tcpdump a macof
│
├── rstpAttack.py              # Útok na RSTP pomocí BPDU spoofingu
├── scapyPackets.py            # Manipulace s pakety přes scapy
│
├── setup.py                   # Instalace jako Python balíček (volitelně)
├── utils.py                   # Pomocné funkce
├── vlanTest.py                # Test chování přepínače v prostředí s VLAN
