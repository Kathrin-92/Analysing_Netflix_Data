# Project: Netflix Data Analysis with Python

## Table of Contents
1. [General Info](#General-Info)
2. [Installation](#Installation)
3. [Demo](#Demo)
4. [Usage and Main Functionalities](#Usage-and-Main-Functionalities)
5. [Contributing](#Contributing)


## General Info
This database was developed as part of a university project (B.Sc. Data Science). The task was to create a database for temporary renting of apartments and bedrooms based on the Airbnb use case using SQL. The database features 20 entities including their associated attributes as well as about 20 data-test-entries for each table. The SQL code for the creation of the db and tables, the INSERT INTO statements for the test data, as well as several queries for testing the database can be found here. 

Before the implementation of the SQL code, the first step in my database design was to determine the purpose of the database. As a crucial component of an online platform that implements the booking and renting of accommodations, similar to a reservation system, the following requirements could be defined in phase 1: The database should allow to store information about guests and hosts, as well as about the available accommodations. This also included information about bookings and related invoices / payments. In addition, ratings were to be submitted and stored. 

As part of the entity relationship model, the information was then divided into tables, the attributes were arranged in columns, and the relationships among the tables were defined. The corresponding entity relationship model can be found here as well. During the development of the SQL database, the ERM was further refined and the final project is slightly changed from the initial plan. 


## Installation

**Requirements:** 
Make sure you have Python 3.7+ installed on your computer. You can download the latest version of Python [here](https://www.python.org/downloads/). 

**Req. Package:**
* pandas
* dash
* dash_bootstrap_components
* ploty.express
* plotly.graph_objects


## Demo



## Usage and Main Functionalities

*Want to know more about your own Netflix behaviour? For test usage you can download your own Netflix data. Just follow this [link](https://www.netflix.com/account/getmyinfo) and Netflix will send you your personal data.*

*Please also refer to the comments within the code itself to get more information on the functionalities of the program.*

#### 0. Preparing the data for analysis
* This part cleans up the original data and prepares it for analysis. 
* In the process, columns that are not needed are dropped. 
* Time data is converted into appropriate time formats and split into several columns. The days of the week are added. 
* In addition, the titles of the movies/series are split (title, season number, episode name). 

---
#### 1. Analysis
* This part of the code is about analyzing the data. 
* We find out how many movies or series were watched over the entire period. We also count the total number of hours Netflix was watched. 
* A pie chart is created that shows which days of the week are watched. 
* In addition, the top 10 series that were watched the longest (in terms of total duration) are displayed. 
* A line chart shows Netflix viewing behavior over the years, counting the total number of hours Netflix was watched. 

---
#### 2. Dash App Layout
* plotly's Dash is now used to create an Interactive Dashboard of Netflix data. 
* The individual graphics and texts are arranged in rows and containers. 
* This part also includes a dropdown menu that the user can interact with. 

---
#### 3. App Callback 
* Here we connect an interactive bar chart to the Dash Components. 
* The chart represents our total annual hours of Netflix watched, grouped by month. The chart is filterable by year. 



## Contributing 
This is my first SQL project. Your comments, suggestions, and contributions are welcome. 
Please feel free to contribute pull requests or create issues for bugs and feature requests.

