###Installation

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

###API Endpoints

**`/restaurants/`**

Fetch a list of restaurants. Optional GET parameters:

* `filter_by`: Method to select restaurants. Options are:
    * `distance`: *Default*. Return restaurants in order of increasing distance from lat/long.
    * `recent`: Return restaurants in order of the most recently selected.
* `lat` and `long`: Latitude and longitude on which to center search. 
                    Default is the coordinates of the Arlington Career Center: lat=38.864428&long=-77.088477
* `count`: Number of results to return.
* `radius`: Size of area to search. Relative to the lat/long values (with same units).

**`/restaurants/<id:int>/inspections/`**

Fetch all health inspections for the restaurant identified by id. Returns inspections in reverse chronological order.