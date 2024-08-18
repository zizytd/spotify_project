# Spotify Project

## Description
This project is an ETL workflow that retrieves user data from the Spotify API and loads it into a SQLite database hosted on Turso.

The goal of the project is to track a user's listening activity on Spotify, including the songs they listen to and the artists performing them.

GitHub Actions is used to schedule and execute the code, running it every 10 minutes. ```10 * * * * ```

## Architecture
![image](images/Spotify%20Project.png)