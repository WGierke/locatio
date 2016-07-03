#locatio

Bring your customer's location files in a consistent scheme and merge shipping tours to neighbouring destinations using our beautiful GUI.

![ui](https://cloud.githubusercontent.com/assets/6676439/16545193/65482e14-4123-11e6-88c9-8412abf102cc.png)


###Before
| Name |Street|Street Addition|Postal Code|City|State|Country|Lat|Long|Opening Times|Time Zone|Building Type|
| :--: |:----:| :------------:|:---------:|:--:|:---:|:-----:|:-:|:--:|:------------:|:------:|:-----------:|
|*Anonymized*|Imperiastraat 8|XXXXX NV/SA| B-1930|Zaventem|BE|
|*Anonymized*|400 Perimeter Center Terrace|Suite 50|GA 30346|Atlanta||US

###After
| Name |Street|Street Addition|Postal Code|City|State|Country|Lat|Long|Opening Times|Time Zone|Building Type|
| :--: |:----:| :------------:|:---------:|:--:|:---:|:-----:|:-:|:--:|:------------:|:------:|:-----------:|
| Cosmopolite|Imperiastraat 8||1930       |Zaventem|Vlaanderen|BEL|50.8799599|4.45349|Mon-Sun: 07:30 - 14:30|UTC+1|House|
|The Capital Grille|Perimeter Center Ter NE 400|Suite 50|30346|Atlanta|GA|US|33.92907|-84.33832|Mon-Thu: 11:30 - 22:00|UTC-5|Apartment|

###Usage
`pip install -r requirements.txt`
