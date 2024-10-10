# Spotify Project

## Description
This project is a serverless ETL workflow that retrieves my user data from the Spotify API, loads it into an SQLite database hosted on Turso, and visualizes the results using Streamlit.

The goal of the project is to track and visualize my listening activity on Spotify, including the songs I listen to and the artists performing them, offering insightful data visualizations for improved analysis.

GitHub Actions is used to schedule and execute the ETL code, running it every 10 minutes ```10 * * * *```.

## Architecture
<p align="center">
  <img src="images/Spotify%20Project.png" />
</p>

## About Spotify API
I made an API call to Spotify to retrieve user listening data using the "Get Recently Played Tracks" endpoint. To access the user's data, authorization is required. This process involves obtaining a refresh token during the authorization, which is then used to generate an access token needed to call this endpoint.

## About Turso
Turso is a cloud-based SQLite database tool built on libSQL, offering 9GB of free storage. I chose Turso because it provides free storage and operates as a serverless service, eliminating the need to manage any servers.

## About GitHub Actions
GitHub Actions is a CI/CD (Continuous Integration and Continuous Deployment) tool created by GitHub to automate software development workflows. I chose to use it because it allows me to schedule the ETL pipeline without the need to manage any underlying infrastructure.

## About Streamlit
Streamlit is an open-source Python framework that enables the quick and easy creation of interactive web applications. It allows developers to build apps using straightforward Python scripts, without requiring front-end expertise. I chose Streamlit because it helps me visualize data from the ETL process efficiently.

[Streamlit App Link](https://spotifyproject-zizytd.streamlit.app/)

## Libraries Installed
- **requests** used for making http requests to the Spotify API.
- **libsql-experimental** used to connect the Turso Sqlite DB.
- **streamlit** used to display the Data.

To install the requirements
```bash
    pip install -r requirements.txt
```

## Limitations/Problems
- Scheduling with GitHub Actions - It doesn't run at the expected time, but typically starts 15 to 20 minutes later. 

## Next Steps
- Carry out further analysis to identify patterns such as:
  - Which genres I listened to more frequently on weekends?
  - Which day of the week I listened to the most music?

## References
### Spotify API
- https://developer.spotify.com/documentation/web-api
- https://developer.spotify.com/documentation/web-api/concepts/authorization
- https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens

### Turso
- https://docs.turso.tech/introduction
- https://docs.turso.tech/sdk/python/quickstart

### GitHub Actions
- https://github.com/features/actions

### Sreamlit
- https://docs.streamlit.io/
