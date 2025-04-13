# SOAP aplikace

Vaším úkolem je vytvořit implementaci serveru a klienta podle dodaného WSDL.
- Bude se jednat o jednoduchou klient/server aplikaci umožňující změnu hesla k uživatelskému účtu
- Sekvence operací bude cca následující:
  - existujicí username
  - verifikace na základě dalšího údaje (klíčové slovo apod)
  - verifikace přes alternativní email (existuje již v profilu)
- zadání nového hesla + jeho verifikace podle pravidel pro heslo
- Aplikace bude umět blokovat další requesty, pokud verifikace 3x neprojde - blokace na 2 minuty
- Odpovídající WSDL zašlu řešitelům / commitnu do jejich gitu

# How to run

Tested with python 3.9

1. Clone the repository
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server
   ```bash
    python server.py
    ```
4. Run the client
   ```bash
   python client.py
   ```
5. Proceed with instructions