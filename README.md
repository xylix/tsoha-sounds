## Itsenäinen tsoha-työ

### Aihe:

Äänien-talletus selainpalvelu

### Käyttö-ohje

TODO: selitä täällä miten sovellusta käytetään

### Toteutettavia ominaisuuksia:
	#### pakollisia korjauksia:

	[ ] Tarkista että projekti täyttää https://hy-tsoha.github.io/materiaali/tekninen_tarkastuslista/ vaatimukset
		* Tarkista myös https://hy-tsoha.github.io/materiaali/arvostelu/

		[ ] validoi user inputit ennen sql inserttejä
		[ ] README:hen käyttöohje
		[ ] Ulkoasun tulee olla _viimeistelty_
	# ennen viimeistä deploymenttiä
	[ ] poista models.py, mutta populoi tietokantaan jotain "valmista dataa"
	[ ] Heroku deployment

#### Tiedettyjä bugeja:
	[ ] Tiedostoja ei siivota kun ne on poistettu kaikista viittaavista projekteista
	[ ] index.html sivulla näkyy "palaa takaisin" näkymä vaikka käyttäjä on jo perusnäkymässä

#### Mahdollisia jatko-ominaisuuksia:
	Endpointin /audio/<id> kannattaisi cachetä saatu tulos, id:t ovat uniikkeja ja tiedostot isoja kannasta haettaviksi 
		* Esim https://flask-caching.readthedocs.io/en/latest/ voisi auttaa tässä
	Projektissa käyttäjä voi lisätä projektiin äänitiedostoja ja kirjoittaa tekstikenttään äänitiedostokutsuja:
		* Äänitiedostot basso_a.mp3 ja basso_g.mp3
		* Tekstikentässä `basso_a basso_g basso_g basso_a` soittaa neljä ääntä

#### Toteutettuja ominaisuuksia:
	[x] Ylläpitäjä voi tehdä kaikkia käyttäjille sallittuja muokkauksia kaikkian käyttäjien projekteihin. Ylläpitäjä voi piilottaa ja poistaa julkaistuja projekteja.
	[x] Lisää auth_required loppuihin endpointteihin joissa tarpeen
	[x] Näytä kommentoijan id:n sijaan nimi
	[x] SQLALchemy modelit ja queryt normaaliksi SQL
	[x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
	
	[x] Käyttäjä voi luoda omia projekteja
	[x] Käyttäjä voi lisätä projektiin tiedostoja
	[x] Käyttäjä voi poistaa projektista tiedostoja
	[x] Käyttäjä voi lisätä omien projektiensa tiedostoja helposti muihin projekteihin
	
	[x] Käyttäjä voi julkaista omia projekteja. Käyttäjä voi perua julkaisun / piilottaa jo julkaistun projektin.

	[x] Käyttäjä voi selata julkaistuja projekteja
	[x] Käyttäjä voi kommentoida / arvostella muiden projekteja
	[x] Käyttäjä voi etsiä projekteja nimen alimerkkijonon perusteella

	[x] Koodin laatu ja tyyli tarkistetaan Pylint- ja Black ohjelmilla

	[x] Käyttäjä voi soittaa projektin äänitiedostoja tai äänitiedostot peräkkäin
		* https://stackoverflow.com/questions/64501684/how-can-i-play-playing-a-mp3-sound-with-flask

#### Korjattuja bugeja:
	[x] Add filesillä voi yrittää lisätä projektissa jo olemassaolevan tiedoston uudestaan


### Lisensseistä:

Esimerkkinä ja sample datana käytettävä äänitiedosto haettu täältä: https://www.free-stock-music.com/fsm-team-escp-neonscapes.html
