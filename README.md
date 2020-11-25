# General Tech Tutorials
Assorted tutorials for working with annoying `python3` packages in both Windows 10 and WSL (Ubuntu 18.04).

# Table of contents
1. [PyODBC/SQLAlchemy for WSL](#pyodbc)
2. [Offline package installations](#offline)
3. [Geopandas for Windows 10](#geopandas)
4. [Installing WSL2 (20.04) without Windows Store](#wsl_install)
5. [Installing multiple instances of SQL server onto a single server/VM/RDP](#mutli_sql)
6. [Download Files with Python](#dl_dataset)
7. [Using command line git on a VM](#git)
8. [SalesForce API](#sf)
9. [Address Regex/Cleaning/Dedupe](#addy)
10. [Automated Emails](#email)
11. [Automating Jupyter Notebooks](#papermill)
12. [Life Saving Regex for data cleansing](#regex)
13. [HTCondor and PostgreSQL](#htcondor)
14. [Webscraping dynamically loaded sites](#webscrape)


## PyODBC/SQLAlchemy for WSL <a name="pyodbc"></a>
Mitigates the error when you are missing `SQL.h` header
```bash
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
exit
sudo apt-get update && sudo apt-get upgrade
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev unixodbc unixodbc-dev
pip3 install sqlalchemy pyodbc
```
Usage:
```python
import pandas as pd
import sqlalchemy
from sqlalchemy import event 

username = r"user"
password = r"pw"
dsnname = r"DB_NAME" # the pyodbc connection name

connection_string = f"mssql+pyodbc://{username}:{password}@{dsnname}"
engine = sqlalchemy.create_engine(connection_string, pool_pre_ping = True, fast_executemany=True)

# Some code that makes it to_sql inserts fast
@event.listens_for(engine, 'before_cursor_execute')
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True
```


## Offline package installations <a name="offline"></a>
How to manually save packages and install them in an offline environment

1. Create a `requirements.txt` file with the list of packages you need
2. `pip3 download -r requirements.txt`
3. Copy downloaded files to offline environment
4. `pip3 install --no-index --find-links /path/to/download/dir/ -r requirements.txt`


## Geopandas for Windows 10 <a name="geopandas"></a>
How to manually save packages and install them in an offline environment

1. Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/
2. You will need 2 different .whl (wheel) files. These are `GDAL` and `Fiona`.
3. Find both of them and download the version corresponding to your device OS and Python. For example, a 64-bit Windows 10 device running `Python 3.7.X` will require this specific file for GDAL. Repeat this for Fiona as well. 

    ![Alt text](https://github.com/akiratwang/Tutorials/blob/main/figures/gdal.png)
    - `cp37` stands for `C-Python3.7.X`
    - `win_amd64` denotes windows devices for a 64-bit architecture 

4. Once they are downloaded, open up `cmd` and `cd` into the directory. 
    - Example: If I downloaded the `.whl` files to the `geopandas_dependencies` folder, then I would use this command:
        - `cd C:\Users\USERNAME\Downloads\geopandas_dependencies`
5. Install the dependencies **in this specific order**:
    - `pip install GDAL-3.1.2-cp37-cp37m-win_amd64.whl` (or the corresponding file you downloaded)
    - `pip install Fiona-1.8.13-cp37-cp37m-win_amd64.whl`
6. `pip install geopandas`
7. Done!


## Installing WSL2 (20.04) without Windows Store <a name="wsl_install"></a>
How to install WSL2 if you have debloated Windows 10 and got rid of the pesky Windows Store.

1. Download the new kernel update here (https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel). 
    - Direct link is (https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
    - If you have a previous installation, you will need to unregister it. If I previously had Ubuntu 18.04, then:
    ```bash
    wsl --list --all
    wsl --unregister Ubuntu-18.04 
    ```
2. Create a powershell script (`.ps1`) with the following code:
```powershell
# this is for wsl2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart

cd c:\

# install 2004 (different url)
# 1804 is https://aka.ms/wsl-ubuntu-1804
Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile Ubuntu.appx -UseBasicParsing

Rename-Item ./Ubuntu.appx ./Ubuntu.zip
Expand-Archive ./Ubuntu.zip ./Ubuntu

cd ./Ubuntu

.\ubuntu2004.exe

$userenv = [System.Environment]::GetEnvironmentVariable("Path", "User")
[System.Environment]::SetEnvironmentVariable("PATH", $userenv + ";C:\Ubuntu", "User")
```
3. Run as admin and you are done!


## Installing multiple instances of SQL server onto a single Server/VM/RDP <a name="mutli_sql"></a>
Issue: SQL server is a type of server which believes it is always _the_ server. This is true most of them when you only have a instance of an SQL server on a single Server/VM/RDP. However, if you want multiple instances of SQL servers, there are specific parameters in order to throttle each SQL server usage.

Initialisation:
1. Launch SQL Server Installation
2.  Click on Installation -> New SQL Server stand-alone installation or add features to an existing installation
3. Install updates if required (optional)
4. Create a new installation **with no features**
5. Enter product key (or a pre-filled product key)

Parameter Set:
1. From the features checkbox, check _Database Engine Services_ and other services where required. You can also change the location of the root instance here.
2. From the Server Configuration Step:
    - Add a suitable engine nad password
    - Tick the _Grant Preform Volume Maintenance Task privilage to SQL Server Database Engine Service_
3. From the Database Engine Configuration Step:
    - Server Configuration -> Tick _Mixed Mode_ and enter the default sysadmin password
    - Server Configuration -> Specify the user(s) who will be the admins of this SQL server
    - Data Directories -> Ensure they are located in the instance root (C Drive by default)
    - Temp Database -> Ensure that the are located where required (some directory or drive with a lot of free space as this can grow)
    - Memory -> Change the max server memory to something like 16GB (16000mb) [Example: 64GB server with 3 SQL Server instances]
    - Accept Terms
4. Install
5. Once completed, verify it works by creating and querying a sample database.


## Download Files with Python <a name="dl_dataset"></a>
How to download files using `urllib`
```python
import urllib

URL = 'www.someurl.com/dataset.csv'
fname = 'some_dataset.csv'
urllib.request.urlretrieve(url, fname)
```


## Using command line git on a VM <a name="git"></a>
Basics of cloning/pushing using commandline git

Cloning:
1. Open terminal 
2. `git clone HTTPS` where HTTPS is the https URL to your GitHub/GitLab repo
3. Enter your credentials
4. Done

Pushing:
1. `cd` into the repo directory
2. `git add .` (add all files in the current `.` directory - you can specify specific files/folders if you want instead with `git add ./updates`)
3. `git commit` (creates a commit) and add your commit description. Use `ctrl+x` to save and `y` to confirm saving
4. `git push` (push to cloud repo)
5. Enter your credentials
6. Done

## SalesForce API <a name="sf"></a>
Setting up SF API for Python
```bash
pip3 install simple_salesforce
```
Usage:
```python
import pandas as pd
import datetime
from simple_salesforce import Salesforce as sf

# credentials
sf_api = sf(username='',
            password='',
            security_token='',
            domain=''
)

# upsert (update + insert)
data = df.to_dict(orient='records')
response = sf_api.bulk.OBJECT_NAME.upsert(data, EXTERNAL_ID_FIELD, batch_size=2000)

results = pd.DataFrame(columns=['success','created','SFID','errors'], index=df.index)
result['OriginalID'] = df['ID']

for col in ('success','created','SFID'):
    result[col] = [i[col] for i in response]

result['errors'] = [i['errors'][0]['message'] if i.get('errors') else '' for i in response]
result['RunTime'] = datetime.now().strftime("%Y-%m-%d %H:%M")    

results.to_sql(TABLE_NAME, engine, index=False, schema='dbo', chunksize=int(3e5), if_exists='append')
```

## Address Regex/Cleaning/Dedupe <a name="addy"></a>
Nice packages for address stuff on top of regex:
- https://github.com/jasonrig/https://github.com/jasonrig/address-net
- https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/details
- https://github.com/seatgeek/fuzzywuzzy
- https://github.com/ethanzhao6/au-addr-parser

## Automated Emails <a name="email"></a>
How to easily send emails. First, set up environment password
```python
import os

os.environ['EMAIL_USER'] = 'example@example.com' # email address
os.environ['EMAIL_PASSWORD'] = 'test' # password
```
Usage (you might have enable developer access on gmail or whatever smtp server first):
```python
import smtplib, os
from email.message import EmailMessage

smtp_server = "smpt.gmail.com:587" # server smtp
from_email, password = os.getenv('EMAIL_USER'), os.environ.get('EMAIL_PASSWORD')

def setup(from_email, pw, smtp):
    server = smtplib.SMTP(smtp)
    server.ehlo()
    server.starttls()
    server.login(from_email, pw)
    server.ehlo()
    return server

server = setup(from_email, password, smtp_server)

# lets say youve got a df with a column for a persons name and their email
for name, to_email in df.values:
    email_msg = EmailMessage()
    email_msg['X-Priority'] = '2' # priorty of email, 2 is important
    email_msg['FROM'] = 'Automated Email Bot' # sender name
    email_msg['Subject'] = 'Automated Email' # subject field
    email_msg['To'] = to_email # send to email 'someone@gmail.com'

    # html formatted email body
    msg = f"""
    <p>Hi {name},</p>
    <p> here's some random text you can write in html <p>
    """
    EMAIL.add_alternative(msg, subtype='html')

    server.send_message(email_msg, from_addr=from_email)

server.quit()
```

## Automating Jupyter Notebooks <a name="papermill"></a>
How to automate jupyter notebooks. Better altneratives include `luigi` and `apache airflow`, but those are not as easy to get working.
```bash
pip3 install papermill
```
Usage:
1. Create notebook(s) for your pipeline
2. Go to View -> Cell Toolbar and enable _Tags_
3. Create a cell with `parameters` as the Tag
4. Add your parameters here
```python
import papermill as pm
from datetime import datetime
import os

PIPELINE_NOTEBOOKS = [
    'notebook1.ipynb',
    'notebook2.ipynb',
    ...
    'notebookN.ipynb'
]

def run(nb):
    timestamp = str(datetime.now().date)
    nb_dir = os.getcwd().replace('\\', '/')
    pm_dir = "./" +  timestamp # directory of papermill output notebooks

    params = {
        'variable1': 'value1',
        'variable2': 'value2',
        ...
        'variableN': 'valueN'
    }
    
    if not os.path.exists(pm_dir):
        os.mkdir(pm_dir)
    
    print(f"""
    Notebook: {nb_dir}/{nb} 
    will be executed to: {pm_dir}/{nb}
    """)

    pm.execute_notebook(input_path=f"{nb_dir}/{nb}",
                        output_path=f"{pm_dir}/{nb}",
                        parameters=params,
                        progress_bar=True
    )

if __name__ == "__main__":
    nb_dir = "./notebooks/pipeline" # notebook dir
    os.chdir(nb_dir)
    
    print("Running pipeline")
    for nb in PIPELINE_NOTEBOOKS:
        run(nb)
    print("Completed.")
```

## Life Saving Regex for Data Cleansing <a name="regex"></a>
The "reg" in regex is prounounced like "regular", not "registry" -> `reg(ular)ex(pression)`.
- https://regexlib.com/?AspxAutoDetectCookieSupport=1

Best ones of note:
- Emails:
    - `"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$"`
- Names:
    - `"^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$"`
- Australian Phone Numbers:
    - `"(^1300\d{6}$)|(^1800|1900|1902\d{6}$)|(^0[2|3|7|8]{1}[0-9]{8}$)|(^13\d{4}$)|(^04\d{2,3}\d{6}$)"`
- Websites:
    - `"^((http|https|ftp):\/\/(www\.)?|www\.)[a-zA-Z0-9\_\-]+\.([a-zA-Z]{2,4}|[a-zA-Z]{2}\.[a-zA-Z]{2})(\/[a-zA-Z0-9\-\._\?\&=,'\+%\$#~]*)*$"`
- Alphanumeric:
    - `"[a-zA-Z0-9]+"`

## HTCondor and PostgreSQL <a name="htcondor"></a>
Docs: https://htcondor.readthedocs.io/en/latest/apis/python-bindings/tutorials/index.html  
Installation:
```bash
pip3 install htcondor classad
python3 -m pip install psycopg2-binary
touch condor_config
export CONDOR_CONFIG=`pwd`/condor_config
```

Python3 for `htcondor`:
- https://research.cs.wisc.edu/htcondor/HTCondorWeek2014/presentations/TheisenT-Python.pdf
- https://htcondor.readthedocs.io/en/latest/users-manual/index.html
- https://research.cs.wisc.edu/htcondor/manual/v8.1/6_7Python_Bindings.html

PostgreSQL with `SQLAlchemy`:
- https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2

## Webscraping dynamically loaded sites <a name="webscrape"></a>
Sometimes you'll find a website that has data you want to scrape, but when you simply load the html there's no table data.
This is because the data is loaded dynamically using JS. 

Some options:
1) Use `selenium`. This requires you have a web driver attached to a path you can run. [Chromedriver](https://chromedriver.chromium.org/downloads) is pretty good, it's what I've used.

Selenium essentially acts as a way to interact with a website through Python. You can click on elements, copy, paste etc. 

Here is a simple example using weather data from New York City:
```python
from selenium import webdriver
d = webdriver.Chrome("<path_to_driver>\chromedriver")
d.get('https://www.timeanddate.com/weather/usa/new-york/historic?month=1&year=2019')

w = {}
# This gets all values in a drop down menu
for i in d.find_element_by_id('wt-his-select').find_elements_by_tag_name('option'):
    i.click()
    print(i.text)
    # will print 1 January 2019, 2 January 2019 etc...
        
    # added sleep time as the webpage itself is really shit and if it updates too fast elements are not loaded correctly
    time.sleep(3)
        
    # add weather
    with get_weather_data(d.page_source, False) as weather:
    w[i.text] = weather
```
*Quick tip:* Depending on your system speed, you'll loop through faster than you'll be able to harvest data if you save. I recommend adding around a 2-3 second sleep each iteration in order to allow time for all the data in the website to fully load.

2) Load the data directly from the ajax request the page makes. [This thread pretty much explains how to grab the data you want using Chrome.](https://stackoverflow.com/questions/52010016/web-scraping-extract-javascript-table-seleniumpython)

Once you have the url it's simply a matter of parsing it, where you can then work with.
The below function parses an ajax requested data into a dictionary, which can then be interrogated and worked with. 
```python
import requests
import json
def get_json_data_from_url(url):
    # set headers for get request (prevents 403 error)
    headers = {'User-Agent':'Mozilla/5.0'}
    
    # send get request and parse response as json.
    text = requests.get(url, headers).text
    data = json.loads(text)
    
    return data
```
