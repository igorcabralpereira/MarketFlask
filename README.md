## Homepage
![Homepage (1)](https://user-images.githubusercontent.com/96249621/217942516-797e4c4b-d6e7-44d6-9f13-889ad9e56112.svg)

## Login / Register
![Login (1)](https://user-images.githubusercontent.com/96249621/217942647-bd9b1d8e-a579-48fa-9388-4aff5273a3f3.svg)
![Register (1)](https://user-images.githubusercontent.com/96249621/217942703-06070035-5d2b-4a21-9506-b59406d6214a.svg)

## Market
![Part1 (1)](https://user-images.githubusercontent.com/96249621/217942929-c328029a-8658-4e00-b91e-21ffe578209b.svg)
![Part2 (1)](https://user-images.githubusercontent.com/96249621/217942945-2fcceed0-3370-4a15-aa98-c3c4e3bcd876.svg)
![Part3 (1)](https://user-images.githubusercontent.com/96249621/217942964-6c7d1c75-8676-4b13-9484-2f5d8ce53fa2.svg)
![Part4 (1)](https://user-images.githubusercontent.com/96249621/217942972-2c64d349-05f4-4829-8101-ddf5737b9652.svg)

## Setup
1. set FLASK_APP=run.py<br />
   set FLASK_DEBUG=1<br />

2. pip install -r requirements.txt

3. python -m flask db init (apenas uma vez para criar a pasta migrations e o alembic caso não exista)<br />
   python -m flask db migrate -m "Initial migration." (caso não exista pasta de migrations)<br />
   python -m flask db upgrade<br />

4. python run.py

5. Caso não houver dados de itens, tem ferramentas para abrir um banco de dados(instance/market.db)<br />
como DBrowser ou SQLite Studio e faça seu INSERT, UPDATE ou DELETE na tabela<br />
de itens.