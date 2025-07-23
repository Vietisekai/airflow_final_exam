### Practice Final Exam 

#### Project Requirement:

The startup TuneStream needs an automated system to orchestrate and monitor their data warehouse ETL workflows. 
*Note:* The pipeline supports two configurations: 
- Loading data from local storage into a local PostgreSQL database, or 
- Loading data from Amazon S3 into Amazon Redshift. 

Using Apache Airflow, the ETL pipeline extracts JSON data files, processes, and transforms 
them, and loads the results into a star-schema relational database according to the chosen setup. 
After the ETL process is finished, data quality checks are conducted to detect any inconsistencies 
in the datasets. 

PS: Hình như file SqlQueries đang bị lỗi ở đoạn không insert được data vào bảng songplays nhưng em chưa fix được :(, DAG cứ chạy đến đoạn check cuối là fail vì k có data.

**Update:** Em đã fix được lỗi này khi sửa file sql_queries.py
