## Itsenäinen tsoha-työ

### Aihe:

Äänien-talletus selainpalvelu

Ominaisuuksia:

	[ ] Ylläpitäjä voi tehdä kaikkia käyttäjille sallittuja muokkauksia kaikkian käyttäjien projekteihin. Ylläpitäjä voi piilottaa ja poistaa julkaistuja projekteja.
	[ ] Lisää auth_required loppuihin endpointteihin joissa tarpeen
	[ ] Tarkista että projekti täyttää https://hy-tsoha.github.io/materiaali/tekninen_tarkastuslista/ vaatimukset

	#### pakollisia korjauksia:
		[ ] SQLALchemy modelit ja queryt normaaliksi SQL
		[ ] queryjen korjauksia (vaikka haettaisiin montaa eri pöytää käytä yhtä queryä. Ohjeita teknisessä tarkastuslistassa kohdassa "Tietokanta-asiat")
		[ ] Näytä kommentoijan id:n sijaan nimi


Mahdollisesti pakollisia?:
	[ ] Käyttäjä voi soittaa projektin äänitiedoston tai äänitiedostot peräkkäin
		* https://stackoverflow.com/questions/64501684/how-can-i-play-playing-a-mp3-sound-with-flask
	[ ] Käyttäjä voi muokata projektia
	[ ] Käyttäjä voi tallentaa muokatun projektin
	[ ] Joku tapa poistaa jotain (projekteja, tiedostoja, kommentteja)


Mahdollisia jatko-ominaisuuksia:
	Projektissa käyttäjä voi lisätä projektiin äänitiedostoja ja kirjoittaa tekstikenttään äänitiedostokutsuja:
		* Äänitiedostot basso_a.mp3 ja basso_g.mp3
		* Tekstikentässä `basso_a basso_g basso_g basso_a` soittaa neljä ääntä

#### Toteutettuja ominaisuuksia:
	[x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
	
	[x] Käyttäjä voi luoda omia projekteja
	[x] Käyttäjä voi lisätä projektiin tiedostoja
	[x] Käyttäjä voi lisätä omien projektiensa tiedostoja helposti muihin projekteihin
	
	[x] Käyttäjä voi julkaista omia projekteja. Käyttäjä voi perua julkaisun / piilottaa jo julkaistun projektin.

	[x] Käyttäjä voi selata julkaistuja projekteja
	[x] Käyttäjä voi kommentoida / arvostella muiden projekteja
	[x] Käyttäjä voi etsiä projekteja nimen alimerkkijonon perusteella


