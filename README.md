# Spotify Project

## Description
This project is a Serveless ETL workflow that retrieves user data from the Spotify API and loads it into a SQLite database hosted on Turso.

The goal of the project is to track a user's listening activity on Spotify, including the songs they listen to and the artists performing them.

GitHub Actions is used to schedule and execute the code, running it every 10 minutes. ```10 * * * * ```

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

## Libraries Installed
- **requests** used for making http requests to the Spotify API.
- **libsql-experimental** used to connect the Turso Sqlite DB.

To install the requirements
```bash
    pip install -r requirement.txt
```

## Limitations/Problems
- Scheduling with GitHub Actions - It doesn't run at the expected time, but typically starts 15 to 20 minutes later. 

## Next Steps
- Analyze the data and create visually appealing dashboards to answer questions such as:
    - What are the top songs the user has listened to?
    - Who are the top artists whose songs the user has listened to?

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
