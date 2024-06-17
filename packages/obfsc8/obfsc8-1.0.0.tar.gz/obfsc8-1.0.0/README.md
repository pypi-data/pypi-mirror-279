# obfsc8
The **obfsc8** package provides a simple way to obfuscate Personally Identifiable Information (PII) found within CSV,  Parquet and record-oriented JSON files that are stored in the Amazon S3 service.
Designed to be used within Amazon Lambda, EC2 and ECS services, **obfsc8** returns a bytes object of the obfuscated file data that can be easily processed, for example by the boto3 S3.Client.put_object function.  


## Setup
Install the latest version of obfsc8 with:
```
pip install obfsc8
```  
  

## obfsc8 functions
The obfsc8 package has one associated function:  

**obfsc8.obfuscate**(  
    ***input_json***: str,  
    ***restricted_fields***: list = [],  
    ***replacement_string***: str = "***"  
)  


### Parameters 

**input_json**
JSON string with the following format:  

    {
        "file_to_obfuscate": "s3://...",
        "pii_fields": ["...", ...]
    }
      

For example, the following requests that the "name" and "email_address" fields be obfuscated in the S3 file found at s3://my_ingestion_bucket/new_data/file1.csv: 
        
    
    {
        "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
        "pii_fields": ["name", "email_address"]
    }


**restricted_fields**
List of protected fields that will not be obfuscated, even if they appear in the 
"pii_fields" key of the input_json parameter.  Defaults to an empty list.

**replacement_string**
    String used to obfuscate all row values for the fields identified in the "pii_fields" key of the input_json parameter, barring inclusion of each field in the restricted_fields parameter list.  Defaults to the string "***".  

### Returns
BytesIO object containing obfuscated file data in the same file format as the input file defined in input_json (CSV, Parquet or JSON).

## JSON limitations
Although this package works with JSON files, only record-oriented JSON is currently compatible.  This type of JSON is structured as a list of dictionaries, each dictionary corresponding to one row of an equivalent pandas DataFrame (see below for DataFrame creation examples).  An example of this type of JSON is as follows:
```
[{"student_id":7914,"name":"Dr Geoffrey Pearce","course":"Data","cohort":2027,"graduation_date":"2027-11-19","email_address":"georgiaarmstrong@example.org"},{"student_id":9225,"name":"Rosemary Lees","course":"Data","cohort":2034,"graduation_date":"2034-05-22","email_address":"elizabethbarker@example.net"},{"student_id":6977,"name":"Miss Barbara Butler","course":"Cloud","cohort":2023,"graduation_date":"2023-01-18","email_address":"bakernathan@example.org"},{"student_id":2565,"name":"Owen Bennett","course":"Cloud","cohort":2021,"graduation_date":"2021-08-30","email_address":"declankelly@example.org"}]
```

## Example usage
#### CSV
Consider a fictional CSV file within the Amazon S3 service, with key name "test_data.csv" inside a bucket that has the name "test-bucket".  This file contains data about students attending software engineering bootcamp courses.  boto3 can be used to download this file, and pandas to put the file data into a DataFrame which can be displayed easily.  First, install the boto3 and pandas packages:
```
pip install boto3
pip install pandas
```
Then to see the contents at the start of the CSV file: 
```
>>> import boto3
>>> import pandas as pd

>>> s3 = boto3.client("s3", region_name="eu-west-2")
>>> get_s3_file_object = s3.get_object(Bucket="test-bucket", Key="test_data.csv")["Body"]

>>> df = pd.read_csv(get_s3_file_object)
>>> print(df.head())
   student_id                    name    course  cohort graduation_date             email_address
0         208      Miss Debra Roberts     Cloud    2023      2042-09-19       keith11@example.net
1        2989  Miss Charlene Marshall      Data    2018      2040-12-01         ngray@example.com
2        8473       Mrs Olivia Rahman     Cloud    2039      2033-07-14      rosstony@example.org
3        6289              Sarah Cole     Cloud    2033      2023-09-19       chloe33@example.org
4        1960          Julian Elliott  Software    2022      2043-01-20  harrisgerard@example.org

```
obfsc8 can be used to load this CSV file from the S3 bucket and obfuscate required fields, by defining the S3 filepath and fields list inside the JSON string that is passed into the obfuscate function.  A file object is returned, which can similarly be displayed as a pandas DataFrame: 
```
>>> import obfsc8 as ob

>>> test_json = """{
...     "file_to_obfuscate": "s3://test-bucket/test_data.csv",
...     "pii_fields": ["name", "email_address"]
...     }"""

>>> buffer = ob.obfuscate(test_json)
>>> df = pd.read_csv(buffer)
>>> print(df.head())

   student_id name    course  cohort graduation_date email_address
0         208  ***     Cloud    2023      2042-09-19           ***
1        2989  ***      Data    2018      2040-12-01           ***
2        8473  ***     Cloud    2039      2033-07-14           ***
3        6289  ***     Cloud    2033      2023-09-19           ***
4        1960  ***  Software    2022      2043-01-20           ***
```
The obfuscated data within the variable "buffer" could be written to an S3 bucket using the boto3 package.  See the Amazon Lambda usage documentation below, for an example of how this could be achieved using the S3.Client.put_object function.
### restricted_fields
The optional restricted_fields parameter can be used to protect key fields from obfuscation, even if the input JSON string contains those fields within the "pii_fields" list.  In the following example the "student_id" field is successfully prevented from being obfuscated, despite its inclusion in the JSON string:
```
>>> test_json = """{
...     "file_to_obfuscate": "s3://test-bucket/test_data.csv",
...     "pii_fields": ["student_id", "name", "email_address"]
...     }"""

>>> buffer = ob.obfuscate(test_json, restricted_fields = ["student_id"])
>>> df = pd.read_csv(buffer)
>>> print(df.head())

   student_id name    course  cohort graduation_date email_address
0         208  ***     Cloud    2023      2042-09-19           ***
1        2989  ***      Data    2018      2040-12-01           ***
2        8473  ***     Cloud    2039      2033-07-14           ***
3        6289  ***     Cloud    2033      2023-09-19           ***
4        1960  ***  Software    2022      2043-01-20           ***
```
### replacement_string
The optional replacement_string parameter can be used to change the string used for obfuscation from the default "***".  The following example shows how a "?" string can be used for obfuscation instead:
```
>>> test_json = """{
...     "file_to_obfuscate": "s3://test-bucket/test_data.csv",
...     "pii_fields": ["name", "email_address"]
...     }"""

>>> buffer = ob.obfuscate(test_json, replacement_string = "?")
>>> df = pd.read_csv(buffer)
>>> print(df.head())

   student_id name    course  cohort graduation_date email_address
0         208    ?     Cloud    2023      2042-09-19             ?
1        2989    ?      Data    2018      2040-12-01             ?
2        8473    ?     Cloud    2039      2033-07-14             ?
3        6289    ?     Cloud    2033      2023-09-19             ?
4        1960    ?  Software    2022      2043-01-20             ?
```
### Parquet and record-oriented JSON processing
#### Parquet
The above exercises can be completed with Parquet files with the addition of some extra steps.  If not already installed, install the fastparquet package:
```
pip install fastparquet
```
Then, assuming the Parquet file referenced in the following test_json string does exist in the referenced S3 bucket, and contains similar data to that contained in the CSV file processed in the CSV examples, above:
```
>>> import pandas as pd
>>> import obfsc8 as ob
>>> from io import BytesIO

>>> test_json = """{
...     "file_to_obfuscate": "s3://test-bucket/test_data.parquet",
...     "pii_fields": ["name", "email_address"]
...     }"""

>>> buffer = ob.obfuscate(test_json)
>>> df = pd.read_parquet(BytesIO(buffer.read()))
>>> print(df.head())
   student_id name    course  cohort graduation_date email_address
0       24227  ***     Cloud    2021      2044-12-07           ***
1       18692  ***     Cloud    2043      2030-04-13           ***
2       22703  ***  Software    2031      2024-01-17           ***
3       30684  ***      Data    2034      2033-11-17           ***
4       10864  ***      Data    2041      2020-10-24           ***
```
#### JSON
Record-oriented JSON file processing is as simple as the CSV case, and does not require the extra packages that Parquet processing does.  Assuming the JSON file referenced in the following test_json string does exist in the referenced S3 bucket, and contains similar data to that processed in the CSV examples, above:
```
>>> import pandas as pd
>>> import obfsc8 as ob

>>> test_json = """{
...     "file_to_obfuscate": "s3://test-bucket/record_oriented_data.json",
...     "pii_fields": ["name", "email_address"]
...     }"""

>>> buffer = ob.obfuscate(test_json)
>>> df = pd.read_json(buffer)
>>> print(df.head())
   student_id name    course  cohort graduation_date email_address
0        6385  ***     Cloud    2037      2033-04-06           ***
1        2680  ***      Data    2019      2041-02-21           ***
2        5567  ***     Cloud    2042      2033-03-18           ***
3        3556  ***      Data    2024      2028-01-29           ***
4        4041  ***  Software    2028      2027-01-29           ***
``` 

## Amazon Lambda usage
### Amazon Lambda Layer creation
If using this package within an Amazon Lambda instance, first create a Lambda Layer that contains the package:
```
mkdir obfsc8
cd obfsc8
mkdir python
cd python
pip install obfsc8 -t .
cd ..
zip -r obfsc8_layer.zip .
```
The resulting obfsc8_layer.zip file should be uploaded to the Amazon Lambda instance as a Lambda Layer.

Note that due to the current size of the obfsc8 package, it is not possible for an Amazon Lambda to have an obfsc8 Layer and an AWS SDK Layer loaded at the same time.
It is however possible to have an obfsc8 Layer and a boto3 Layer loaded at the same time.
If you wish to use boto3 within an Amazon Lambda, create an additional boto3 Lambda Layer by repeating the steps above, but replacing "obfsc8" with "boto3", and uploading the resulting .zip file to the Lambda as a Lambda Layer.  


### Amazon Lambda lambda_handler example code
The following is an example of possible usage of obfsc8 within an Amazon Lambda, with boto3 handling the writing of the obfuscated file data to an S3 bucket: 
```
import json
import boto3
import obfsc8 as ob


def lambda_handler(event, context)
    try:
        obfuscation_instructions = json.dumps(event["detail"])
        buffer = ob.obfuscate(obfuscation_instructions)
        
        source_filepath_elements = event["detail"]["file_to_obfuscate"].split("/")
        source_filepath_elements[-1] = "obfs_" + source_filepath_elements[-1]
        obfuscated_file_key = ("/").join(source_filepath_elements[3:])
        
        s3 = boto3.client("s3", region_name="eu-west-2")
        put_response = (s3.put_object(
            Bucket="test-bucket",
            Key=obfuscated_file_key, Body=buffer))
            
        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully obfuscated: {obfuscation_instructions}")
        }
    
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to obfuscate file: {e}")
        }
```

A test event similar to the following can be used to check the above code functions correctly:
```
{
  "detail-type": "File obfuscation event",
  "source": "aws.eventbridge",
  "detail": {
    "file_to_obfuscate": "s3://source-bucket/2024/test_data.csv",
    "pii_fields": [
      "name",
      "email_address"
    ]
  }
}
```