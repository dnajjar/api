## Chartbeat Take Home Code Challenge

### How to run

In order to run this API, clone this repository and then do the following: 

1. Run `pip install -r requirements.txt`.
2. Modify the `file_path` variable in `config.py` to point to the location of the repository in your environment .

3. Navigate to that directory and run `python scheduleCron.py` to add a new job to your crontab. Alternatively, manually add `* * * * * /path/to/python /path/to/api/get_concurrencies.py` to your crontab file by typing `crontab -e` in your terminal. 

4. Wait 2 minutes to allow for the database to populate, then run `python app.py` and navigate to `http://localhost:5000/api`. You should now see the result from the API request.

5. Delete cron job from crontab file.

### Wishlist Items

Given more time, I would have liked to do the following:

1. Write unit tests for `app.py` and `get_concurrencies.py`

2. Explore the possibility of a non relational database since it seems to lend itself better to the structure of the data stored

3. Not hardcode the API in the config.py file 

4. Use an ORM rather than raw SQL

5. Implement error handling for the cases where the requests to the Chartbeat API time out or fail

### Additional Thoughts 

This implementation of the API stores an initial set of values for a given path, and on each subsequent API request updates the number of visitors and stores a visitor delta for that path if it appears in the response. Uniqueness is verified by the path alone, but it might be more useful to verify a combination of both path and page title. What's more, relying on the number of visitors from minute to minute is a poor proxy at best for actual page popularity for a number of reasons: 

- User interactions on a page could be a better indicator of actual popularity than just the number of visitors
- Looking at a minute to minute differential will almost certainly ignore general trends over time, and we could probably get a more insightful measure by taking a moving average of concurrency increases per minute over the past 10 minutes
- What's more, if the 100 pages being returned are not always the same, and are based on the 100 most popular pages at any given time, this method will not be useful for the case where a page drops off the rankings entirely and then reappears.
