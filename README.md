# General Tech Tutorials
Assorted tutorials for working with annoying `python3` packages in both Windows 10 and WSL (Ubuntu 18.04).

# Table of contents
1. [PyODBC/SQLAlchemy for WSL](#pyodbc)
2. [Offline package installations](#offline)
3. [Geopandas for Windows 10](#geopandas)
4. [Installing WSL without Windows Store](#wsl_install)
5. [Installing multiple instances of SQL server onto a single server/VM/RDP](#mutli_sql)
6. [Download Files with Python](#dl_dataset)
7. [Using command line git on a VM](#git)
8. [SalesForce API](#sf)
9. [Address Regex/Cleaning/Dedupe](#addy)


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

    ![Alt text](./figures/GDAL.png)
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


## Installing WSL without Windows Store <a name="wsl_install"></a>
How to install WSL if you have debloated Windows 10 and got rid of the pesky Windows Store
1. Create a powershell script (`.ps1`) with the following code:
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

cd c:\

Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu.appx -UseBasicParsing

Rename-Item ./Ubuntu.appx ./Ubuntu.zip
Expand-Archive ./Ubuntu.zip ./Ubuntu

cd ./Ubuntu

.\ubuntu1804.exe

$userenv = [System.Environment]::GetEnvironmentVariable("Path", "User")
[System.Environment]::SetEnvironmentVariable("PATH", $userenv + ";C:\Ubuntu", "User")
```
2. Run as admin and you are done!


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
    - Tick the _Grant Preform Volume Maintenance Task privilage to SQL Server Database Engine Service*
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


## Using command line git on a VM <a name="#git"></a>
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
Nice packages for address stuff:
- https://github.com/jasonrig/https://github.com/jasonrig/address-net
- https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/details
- https://github.com/seatgeek/fuzzywuzzy
- https://github.com/ethanzhao6/au-addr-parser
