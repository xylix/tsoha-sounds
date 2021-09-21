## Itsenäinen tsoha-työ

### Aihe:

Äänien-talletus selainpalvelu

### Käyttö-ohje

Sovellusta voi käyttää osoitteessa https://tsoha-sounds.herokuapp.com/

Sovelluksen etusivulta voi kirjautua sisään tai rekisteröityä. Muu toiminnallisuus ei ole käytettävissä kirjautumatta.

Sisäänkirjautumisen jälkeen sovelluksen päänäkymässä voi tarkastella olemassaolevia projekteja, poistaa projekteja joihin oikeudet, hakea projekteja, luoda projektin tai kirjautua ulos.

Varsinainen toiminnallisuus on projektien sisältä. Kaikissa projekteissa joihin käyttäjällä on pääsy voi kuunnella projektiin kuuluvia tiedostoja, lukea kommentteja ja kommentoida.

Projekteissa joihin käyttäjällä on muokkausoikeudet (omat projektit ja admin-käyttäjillä kaikki projektit) voi lisätä tiedostoja, poistaa tiedostoja ja vaihtaa projektin julkaistu/julkaisematon statusta.


### Koodista

Projekti on organisoitu python moduuleihin. Sovelluskoodi löytyy projektin juuren sisältä kansiosta App/. 

Projektin rakenne:
* / 
	* README.md
	* schema.sql
		* Projektin sql-skeeman luontiskripti
	* pylintrc
		* Projektin tyylin tarkastamiseen käytettiin pylint lintteriä, josta otettiin muutamia sääntöjä pois päältä. Koodi formatoitiin `black` työkalulla josta johtuen rivipituuden tarkastaminen jätettiin sille. Lisäksi joitain muita moduulien ja funktioiden dokumentointiin liittyviä tyylisääntöjä kytkettiin pois päältä.
	* Procfile
		* Herokun deploy-resepti.
	* requirements.txt
		* Sovellyksen ajoon tarvittavat dependencyt.
	* initial_data.py 
		* Voidaan ajaa tietokannan alustuksen jälkeen, lisää sinne esimerkkidataa
	* App/
		* app.py on sovelluksen päätiedosto
		* helpers.py sisältää apufunktioita ja decoraattoreita.
		routes/
			* Flask-sovelluksen routeja, jaettuna sovelluksen toiminta-alueen mukaan.
		static/
			* Projektin favicon ja CSS-tiedosto
		templates/
			* HTML-pohjat näytettäville sivuille



### Ominaisuuslista ja toteuttamattomat ominaisuudet:

#### Tiedettyjä bugeja:
	[ ] Tiedostoja ei siivota kun ne on poistettu kaikista viittaavista projekteista
	[ ] index.html sivulla näkyy "palaa takaisin" näkymä vaikka käyttäjä on jo perusnäkymässä
	[ ] Käyttäjäsyötteiden pituuksia ei validoida ennen sql-inserttejä


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
