# Purpose

Bring data from Oracle DWH database to the Cloud ( Google Cloud Storage). Data should reach the cloud storage buckets in parquet format.

# Prerequisites
Python version >= 3.8
You have to download and use and instant Oracle client ( download it and add it in the workdirectory)s
```
https://www.oracle.com/database/technologies/instant-client.html
```

Create a python virtualenv and activate it

```
    python -m venv env
    source env/bin/activate
```

If you want to close/deactivate the virtualenv, just run this command ( make sure you are in your working env/directory)
```
    deactivate
```

Install required python packages. If you are on VPN it might not work, disconnect and install packages and you can connect back to it afterwards.

```
    pip install -r requirements.txt
```

# How to setup and run
Make sure that you can connect to Oracle database.

If you want to run the tool:

```
    python tool.py
```

If you want to run the tests:
```
    pytest -s
```


Monitoring!

```

Metrics to push in gcp

```