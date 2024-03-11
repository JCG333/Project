# Vision

The vision of this project is to develop a functional and user-friendly website and a database where information about wind turbines is retrieved and displayed. The project requires that each turbine has location information, as well as both current status with images and historical data linked to it stored in the database.
A database needs to be set up. Additionally, an API from SMHI must be implemented to gather weather data. The website needs to be built with a login page, a filtering and search page for the user's wind turbines, pages where the selected turbine's status is displayed with images and weather data from SMHI. History should be available for the different turbines with older weather data from SMHI.

# Install and Startup

It would be wise to install miniconda or a similar package manager and configure it to run with your prefered IDE.

1. Open the terminal of your choice. (either for your local machine or server instance)


2. Start by cloning the repository to your local machine or server instance.

```
git clone https://github.com/JCG333/Project
```

3. Relocate into the project directory **Project** that you've just cloned.

4. Run the following command twice in the terminal. (this will build the docker image and start the containers)

```
docker-compose up --build -d 
```

5. (optional) to ensure functionality, run the following command to make sure all containers are running.

```
docker ps
```

# How to use

The portal will (unless instructed otherwise) be exposed to port 4000. (this can be changed in docker files)

## Locally

- Once you've followed the steps in **Install and startup**, go to the following address (https://localhost:4000) to reach the portal login.

## Server

- Once you've followed the steps in **Install and startup**, the portal login should appear at the public ip of your server instance.

# For developers

## Improvements

- **Security:** Altough security was a point of focus during the development, there are many possible security improvements that can be done to ensure the integrity of the application.
- **Machine learning:** Machine learning is a big part of the project, one that we didn't quite explore to the fullest extent. The images taken by the cameras should use machine learning to identify the ice and snow accumulation on the turbines.

## What should be done next
- The charts displayed on the turbine pages should display weather data 12 hours before and 12 hours after the current point in time. At the moment it retrievs all weather data for the specific turbine.
- The _Risk_ variable should display the risk of a specific turbine(this variable should be calculated using some formula given by project handler). 
- The Account-, Settings-, Help & Support pages could need some visual- and feature improvements.
- The login should require that the email input should be of a specific format to be valid(ex. Hello@World.com).
- Search button on search page could be re-designed to work better in more dynamically with different window sizes.
- Language changes should apply to turbine list entries.

_Note: The branch light/dark mode contains fixes for the visual and feature improvments for the webpage and the languge changes for the turbinelist. There was not enough time to merge it with the main and make sure that all features worked   
# Tech stack
_Note: minor packages can be found in requirements.txt_


Docker | PostgreSQL | Python | Flask | HTML | CSS | JavaScript | SQLAlchemy 







