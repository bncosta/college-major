# CollegeMajor

By Aaron Shah and Brian Costa

Web application allowing easy search and analysis of expected earnings by major for American universities. Searches can be done
by university or major name, with detailed graphs, tables, and university insights. Salary data for over 300 unique majors across 5,500 public, private non-profit, and private for-profit universities. Over 40,000 total earnings records.

Data provided by the Department of Education's [College Scorecard](https://collegescorecard.ed.gov/). Explore their data [here](https://collegescorecard.ed.gov/data/). 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Required tools.

```
Python 3.5 or greater
Django 2.0 or greater
PostgreSQL Version 11
Django-Autocomplete-Light 3.5.1 or greater
Reccommended IDE: Pycharm (for great Django support)  
```

### Installing

Installation consists of two major parts. Configuring Python and Django to run the provided web application,
and configuring the database. 

1. Clone the project. Ensure you have the software required in the prerequisites. Run the project as a Django server.
2. Create a database in PostgreSQL called *collegemajor*. Running the PostgreSql application, psql, in the command line,
run the dump file *data.sql*, [available here](https://drive.google.com/drive/folders/13W0sOaTGrPlGcmdazTM-sKqxiuDbtxAA?usp=sharing). After the successful creation of the database, 
create a file at the root of the project called *passwords.py*. Add the following variables:

- DATABASE_USERNAME = {name of username configured for database CollegeMajor}

- DATABASE_PASSWORD = {name of password configured for database CollegeMajor}

- SECRET_KEY = {name of your secret key} 

You can generate a secret key for this project with the following command from the command line.

```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

The Django web application will run on on the localhost on port 8000, and PostgreSQL will run on port 5432.


## Deployment

To deploy, follow standard operating procedures for deploying a Django application and database.

Use WhiteNoise Django extension to render static files

Remember to update the database connection host in settings.py.

## Updating the Data

College Scorecard occasionally updates their data. To update the database with new records from College Scorecard,
 complete the following. 
 
 1. Download *Most Recent Data by Field of Study* from [here](https://collegescorecard.ed.gov/data/),
  and convert the file to .csv.
 2. Delete all rows where the field *MD_EARN_WNE* is **PrivacySuppressed**.
 3. In the database, remove (if present) the table *collegemajor*, and recreate the table with the following script. 
 
     ```
    CREATE TABLE collegemajor
    (unitid varchar, opeid6 varchar, instnm varchar, 
    control varchar, main varchar, cipcode varchar, cipdesc varchar
    , credlev varchar, creddesc varchar, count varchar, debtmedian varchar
    , debtpayment10yr varchar, debtmean varchar, titleivcount varchar, earningscount varchar, md_earn_wne varchar
    , ipedscount1 varchar, ipedscount2 varchar, id varchar);
    ```

 4. Run the following to populate this table with the data from the .csv 
 
    ```
    \COPY collegemajor FROM '<path>' WITH (FORMAT csv);
    ``` 

    Note: Replace <path> with the absolute path to the .csv file,
     and run this command from PostgreSQL's psql command line.
    
  5. In the database, change the data for columns *cipdesc* and *instnm* to be only lowercase.
   Do so with the following two commands.
   
       ```
        UPDATE collegemajor SET cipdesc=lower(cipdesc)
        UPDATE collegemajor SET instnm=lower(instnm)
       ``` 
  6. Database should be successfully updated.
 
 ## License

This project is licensed under the GNU General Public License.
