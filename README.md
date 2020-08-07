# python-flask

## Funds Calculator


## All about investments.

### We have created a one page application, where we have provided various menu options which will help you to redirect on Axis Mutual Fund Website and we also have provided you option to verify your Investment value you have made previously.
![HomePage](Funds%20Calculator%20/screenshots/1_Homepage.png)

### We have provided two options where we can search Fund by Category or by Code. And we have added validations in case we provide wrong input or in case we miss to fill the input box.
![Input](Funds%20Calculator%20/screenshots/2_Input.png)

### Once we provide a valid input, then we can see the result in table with the current investment value
![Output](Funds%20Calculator%20/screenshots/3_Output.png)

## Approach Used

### 1: We first have written a code which is used to convert text file into the json format, where we have created two json file one for storing the list of funds and second is use for storing value.

### Fund List -
![FundList](Funds%20Calculator%20/screenshots/4_FundList.png)

### Fund Data -
![FundData](Funds%20Calculator%20/screenshots/5_FundData.png)

###2: Then we worked on the view, where we choose to use jinja templating, to pull dynamic data in selection box.

###3: Then we made use of Flask framework, to pull data on the templates.
