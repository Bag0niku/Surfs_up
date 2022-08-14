# Surfs_up
Analysis of weather in Hawaii

## Resources:
- Data: hawaii.sqlite
- Software:
  - Python 3.7.14, Pandas 1.4.2, Numpy 1.21.5, SQLAlchemy 1.4.32, Flask 1.1.2
    - Sometimes Windows PC's need psycopg2-binary to run SQLAlchemy
  - Jupyter notebook (notebook server 6.4.8, Ipython 7.31.1)

## Flask API
hawaii.sqlite contains temperature and precipitation data for 9 weather stations across the island of Ouahu, Hawaii from January 1, 2010 to August 23, 2017.  I took my initial data exploration and analysis from the climate_analysis.ipynb file and turned it into an API with python's Flask framework.

## Challenge
While Most of the analysis was conducted only on the last year of available data. I did combine every month of june into it's own table and did the same with December. Comparing the two months together the first point noticed is that there is not much difference between the 2. 
 - Junes temperatures are only slightly higher than December
   - 25%, 50%, 75% and Maximum data points are between 2-4 degrees apart.
   - The average is 3 degrees apart.
 - December termperatures have a wider range with a minimum of 56 instaed of June's 64.
 After graphing them it is easier to see that average daily temperature is about 5 degrees cooler in December than June.