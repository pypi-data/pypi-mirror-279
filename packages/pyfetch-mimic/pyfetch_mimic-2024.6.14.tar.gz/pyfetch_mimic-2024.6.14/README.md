# pyfetch-mimic
- This is a simple module that mimics `pyodide.http.pyfetch` to make local development for `shinylive` projects easier. It may work with `pyodide` in general, but that use case hasn't been tested.
- For more information on Shinylive for Python, and general information on how to use additional third party libraries (like this one), see: https://shiny.posit.co/py/docs/shinylive.html

## Install
- PyPI: `pip install pyfetch-mimic`
- Vendoring:
  - Copy `pyfetch_mimic.py` into your own project

## How to use
- Include the following conditional import statement at the beginning of the module that will use `http.pyfetch`:
    ```python
    import sys
    if "pyodide" in sys.modules:
        from pyodide import http
    else:
        from pyfetch_mimic import http
    ```
- Use `http.pyfetch` as usual
- **NOTE**: This is a *work in progress* and does not support all `pyodide.http.pyfetch` functionality yet. I use this in my own production work, and the functionality that currently exists is simply the functionality that I need. If there is a need for additional functionality, please open an issue or pull request.

## pyfetch examples
- These should all work with python `pyodide.http.pyfetch` and `pyfetch_mimic.http.pyfetch`

```python
# Download, save extracted file to local virtual fs
import sys
if "pyodide" in sys.modules:
    from pyodide import http
else:
    from pyfetch_mimic import http

async def sample():
    response = await http.pyfetch("https://some_url/myfiles.zip")
    await response.unpack_archive()
```

```python
# Download text file to local virtual fs, load into pandas
import pandas as pd
import sys
if "pyodide" in sys.modules:
    from pyodide import http
else:
    from pyfetch_mimic import http

async def sample():    
    response = await http.pyfetch(url())
    with open("test.json", mode="wb") as file:
        file.write(await response.bytes())
    df = pd.read_json("test.json")
```

```python
# Download text file into BytesIO memory buffer, load into pandas
from io import BytesIO
import sys
import pandas as pd
if "pyodide" in sys.modules:
    from pyodide import http
else:
    from pyfetch_mimic import http

async def sample():
    response = await http.pyfetch("<URL>")
    buf = BytesIO(await response.bytes())
    df = pd.read_json(buf)
```

## Testing

### Install Test Dependencies
- `pip install -e '.[tests]'`

### Run regular tests (verifies test endpoints and tests `pyfetch-mimic`)
- activate venv: `source .venv/bin/activate`
- start fastapi app: `python3 src_test_webserver/main.py`
- run pytest: `pytest -vv -x test`

### Run pyodide tests with pyfetch calls written identical to `pyfetch-mimc`

#### Manually
- activate venv and start test fastapi app using step above
- export shinylive app: `shinylive export ./test/tests_shinylive ./src_test_webserver/shinyapps`
- open shinylive app in edit mode: `http://localhost8000/apps/edit/`
- Click "Run tests"
- If all function names at the bottom are followed by "passed", then everything should be ok

#### Using Robot Framework
- activate venv
- export shinylive app: `shinylive export ./test/tests_shinylive ./src_test_webserver/shinyapps`
- run robot: `robot test/robot_tests/`
