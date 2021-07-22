Instructions
===========

* create virtualenv
* activate vitualenv: source bin/activate
* install dependences: pip install -r requirements/base.txt.
* execute command `python manage.py migrate --settings=config.settings.base` to create datatables
* run project django
* open Postman, set the url `http://localhost:8000/get-token/` and parameters form-data to generate and save access_token
  ```
  -grant_type
  -redirect_uri
  -client_id
  -client_secret
  -code
  ```
* access to `http://localhost:8000/`
* copy and paste access_token in input and clic button `Search`
