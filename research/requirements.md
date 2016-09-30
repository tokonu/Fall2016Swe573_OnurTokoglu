# Project Requirements

1. User Profile Related
    - 1.1 User will register to the system
    - 1.2 User will input (Date of Birth, Gender, Height, Weight) information upon registration and will be able to modify these fields later.
        - 1.2.1 Historical data of weight info will not be kept
        - 1.2.2 Body Mass Index (BMI) will be calculated using Mass(kg)/Height(m)^2 
        - 1.2.3 Daily calorie requirement will be calculated (see 4.1.2)
2. Nutrition Related
    - 2.1 User will input food consumed
        - 2.1.1 User will enter a search text and related foods will be listed (see 2.2.1)
        - 2.1.2 User will select food and enter amount
        - 2.1.3 Historical data of consumed food will be kept
    - 2.2 Nutrition info will be taken from USDA Food Database - [Link](https://ndb.nal.usda.gov/ndb/doc)
        - 2.2.1 Food names will be queried by text and related food name-id pairs will be received
        - 2.2.2 Nutrition info will be received from an api call made with food id
    - 2.3 Nutrition value will be calculated according to 2.1 and kept historically
        - 2.3.1 Percentage to daily recommended value will be shown (see 4.2.1)
3. Activity Related
    - 3.1 User will input activity
        - 3.1.1 User will enter a search text and related activities will be listed
        - 3.1.2 User will select an activity from the list and enter amount
        - 3.1.3 Burned calories will be calculated by interpolating user weight with available data (see 3.2)
        - 3.1.4 Historical data will be kept
    - 3.2 Activity info will be taken from [here](http://www.nutristrategy.com/activitylist4.htm)
        - 3.2.1 Activity list will be kept in a local database
        
4. Reporting Related
    - 4.1 User balance (calories burned, taken, basal metabolic rate) will be shown in a selected date intervals
        - 4.1.1 Basal metabolic rate will be calculated according to [formula](https://en.wikipedia.org/wiki/Harris–Benedict_equation)
    - 4.2 Nutritional data will be provided with the recommended amounts in a selected date interval
        - 4.2.1 Recommended values will be calculated [according to](http://www.fda.gov/Food/GuidanceRegulation/GuidanceDocumentsRegulatoryInformation/LabelingNutrition/ucm064928.htm)
    - 4.3 Statistical information about food consumption will be provided in a selected date interval
    - 4.4 Graphs will be provided to make reports visually appealing
    
5. Other
    - 5.1 Backend will be developed using Python+Flask
    - 5.2 Frontend requirements not specified, will be decided
        
        
# Questions

### Related to 1
    - Can we use 3rd party login providers
    - Should user be able to use the system without registration
    - When should the session expire
    - Where will we use the calculated BMI. Should we keep a historical data of BMI?
    - How should the goals be used in the system
    
### Related to 2
    - Should we keep local cache of the nutrition info
    - Is it ok to only offer si units
    - Should we keep protein, lipid etc info seperately (vitamins, minerals?) or just kcal?
    - Should we do search recommendation while the user is typing
    - Should we suggest previously entered foods
    
### Related to 3
    - Should we aggregate similar activities while reporting? (Walking 1mph and Walking 2 mph)
     
### Related to 4
    - Should we provide time information will be provided on selected food entries (i.e. select cheese and see the dates you have eaten cheese)
    - Should we provide hour based information (i.e. 300 kcal at 1pm, 500 kcal at 5pm)
    
    
    
    
    
    
    
    
    