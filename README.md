To setup Python (need Python>=3.6):

```bash
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To setup database (need Spacialite installed):

```bash
python db_setup.py
```

To run app:

```bash
FLASK_APP=foodapi flask run
```