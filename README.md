# NBA HIMdex

- Project: nba-himdex
- Web App: https://nbahimdex.web.app/
- Version: 1.0.0
- Version Date: June 5, 2024
- Author: Eric Tria
- Email: ericmtria@gmail.com

### Project Overview

- An experimental method to measure which NBA Players are HIM based on some user input.
- Read more about the project here: https://nbahimdex.web.app/about

## Data

- NBA data is sourced using the [nba_api](https://github.com/swar/nba_api) library.
- Includes data from the 2008-09 season to the 2022-2023 season.
- Feature engineering was done using SQL and stored in Google BigQuery.
- A K-Means clustering model was used for generating the HIM groups.

## Deployment

- A Flask app serves as the main UI for interacting with the dataset.
- The app is deployed on Google Cloud Run and hosted through Firebase.

### Run Flask Locally:

- export FLASK_APP=main
- export FLASK_ENV=development
- flask run

## Example Usage

1. Select a season.
2. Select the player from that season who you believe is HIM.
3. Click on the 'Load HIM Group' button to load players who impact the game in a similar ways. These are the players who are also HIM by your definition.

![Example 1](/static/images/example1.png)

- In the example above, if LeBron James in 2016 is your definition of HIM, then the other players in the resulting table are also HIM.

- Also, LeBron in 2008-09 was one of one:

![Example 2](/static/images/example2.png)

## Interesting Cases

- Players who played on different teams within a season may have different HIM groups for each team that they played on. For example:

- JR Smith on the Knicks in 2014-15:

![Example 3](/static/images/example3.png)

- JR Smith on the Cavs in 2014-15:

![Example 4](/static/images/example4.png)

- JR was in 2 very different groups based on the team that he played on that season.