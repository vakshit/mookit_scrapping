# mookit_scrapping

It uses selenium and chrome browser to get the HTML page.
After that BeautifulSoup is used to get all the required fields.

## Usage:

#### Step 1

```bash
bash credentials.sh
```

It will ask for username as password of the user and store in a yml file. This process is required only for a new user

#### Step 2

Some modules are requiqred to work, for it run the following commands:

```bash
pip3 install selenium
pip3 install bs4
pip3 install pyyaml
pip3 install re
```



#### Step 3

```bash
python3 main.py
```

It will ask for course code and number of lectures.
Once input is provided, it opens chrome browser does all stuff and writes all data to `out.csv`

