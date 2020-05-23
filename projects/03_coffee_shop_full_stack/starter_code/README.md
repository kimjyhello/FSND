# Coffee Shop Full Stack

This is the new digital menu for Uda-Spice Latte Cafe, where you can view the menu and see graphics representing the ratios of ingredients in each drinks.
Baristas can log in to see the recipe for each menu, and the manager can log in to add an item to the menu, update details on the item and delete items from the menu. 


## About the Stack

### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
