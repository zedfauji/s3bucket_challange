# s3bucket_challange
Code for reading file over s3 and matching it based on Lat and Long.

Writeup

Task :- Given task could be divided into below mentioned modules 
1.Download from S3 and Addition of Headers :-  Download the required files from s3 with proper permission and data headers as it wasnt present in the file, headers were added which will makes it easy to categorize the contents of csv files as a list of dictionaries. All the data from csv is exported as dictionary and then formed as a list , in order to perform optimised iteration and sorting. 

2. Iterations of Sites.csv :- As this will be the source file for the comparison and searching, id's needed to be counted as it will tell how many entries are there in the file for what we need to perform searching. First iterator extract each id along with its site name and lat + long for comparing with images.csv

3. Iteration of images.csv :- This files contains lat + long which were extracted as pointers to be compared with . each entry of lat + long were iterated and sent for harvesine function in order to calculate the distance between the site lat + long and image lat + long. this distance will tell which site is nearby to which image

4. Taking a source vector area :- This vector area ( in this program take as 5 KM) is required to check the nearby status of a site with the image lat + long. This is the circle diameter assumed in ordered to get the nearby solutions

5. Date :- Dates were also matched along with site data in sites.csv with Image data in images.csv to see if those were conjunctive. 

6. Sorting :- After the results were added in a list there were sorted based on their Lat value

7. Uploading to S3 along with ACL Permission :- After creating the file from final result dict (list file ) in csv format, files were uploaded to their respective S3 bucket as Object under respective directory along with ACL Permission. 


Improvements 

1.  More better handling of csv format files , for ex. iterating over sites.csv , rather than counting id's better way to iterate through number of rows
2.  Writing dict to csv format file. 
3. Performing dates calculation to check if dates are sames
4. uploading to s3 with more defined and explained permissions
5. Searching , comparing and sorting based on distance calculated between 2 files, it requires a more complex lambda function which will reject the results at the time of sorting while performing the calculations also. 

Note :- 

1. Expected , that the code isn't optimized, the more the source file size will be , more it will take time and memory to process. 

