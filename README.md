
# Internet of Things and Services

Ovaj projekat je mikroservisni projekat, koji obradjuje podatke o Londonskoj strujnoj mrezi. 




## Komponente

Ovaj projekat sadrzi sledece komponente:

- PostgreSQL bazu podataka

- SensorGenerator: Python klijent koji salje objekte preko POST HTTP zahteva na Gateway, koji simulira aktivnost nad servisima.

- Gateway: Python FastAPI REST API mikroservis koji sluzi kao pristupna tacka celom sistemu. Implementira gRPC protokol, i sluzi kao klijent za prosledjivanje zahteva na servis koji direktno kontaktira bazu.

- DataManager: C# ASP.NET gRPC mikroservis koji prima zahteve sa Gateway-a i kontaktira bazu podataka. Preobradjuje zahteve iz formata koji su odgovarajuci za tekstualni dokument, u format koji je odgovarajuc za PostgreSQL bazu. Implementira MQTT klijent za komunikaciju sa ostatkom mreze mikroservisa.

- Migration: Privremeni kontejner koji se aktivira pre DataManager mikroservisa, koji postavlja Entity Framework Core migraciju na PostgreSQL bazu podataka.

---

- Mosquitto: Kontejnerizovan MQTT broker.

- EventManager: C# ASP.NET MQTT mikroservis koji prima notifikacije od DataManager servisa, i prosledjuje preko MQTT elektronske dogadjaje sa iznad-prosecnim naponom.

---

- NATS: Kontejnerizovan NATS broker.

- Analytics: Node.js MQTT/NATS mikroservis za obradu objekata sa visokim naponom. Pri primanju poruke preko MQTT kanala, objekat se prosledjuje preko HTTP poziva MLAAS mikroservisu, koji prosledjuje nazad klasu objekta. Nakon toga, Analytics objavljuje preko NATS kanala klasu objekta. 

- MlAAS: Python FastAPI mikroservis koji obavlja prostu analizu objekta.

---

- MQTTNATSClient: Python klijent pisan sa NiceGUI biblotekom za reaktivan UI dizajn, koji implementira MQTT i NATS klijente za prijem poruka sa EventManager i Analytics mikroservisa.


## Deployment

U folderu Analytics, pokrenuti:

```bash
 npm install
```

U folderu DataManager/DataManager/DataManager, izvrsiti:
```bash
 dotnet ef migrations bundle --self-contained -r linux-x64
```
i prebaciti u folder /Migration.

Za pokretanje ovog projekta, potreban je **docker compose.**

Projekat se moze pokrenuti komandom:

```bash
 docker compose up -d
```
