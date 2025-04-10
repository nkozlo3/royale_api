# Clash Royale Deck Creator

This is a Flask application that allows users to create and manage Clash Royale decks. It provides features to search for meta decks, generate war decks, and fetch card data based on rarity. The application integrates with the Clash Royale API to fetch player and deck data and stores it in a database.

## Table of Contents

- [Technologies](#technologies)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)

## Technologies

- Python3
- Flask
- SQLAlchemy
- MySQL
- Clash Royale API
- JavaScript
- HTML/CSS
- AJAX

## Features

- Search for meta decks based on card names.
- Generate war decks with card rarity filters.
- Fetch and display card data by rarity.
- Store and manage decks in a database.
- Update meta decks using the Clash Royale API.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/royale-api.git
    cd royale-api
    ```

2. Set up a virtual environment and install dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    flask db upgrade
    ```

4. Configure the `.env` file with your Clash Royale API key:
    ```env
    ROYALE_API_KEY=your-api-key
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Usage

- Open your browser and go to `http://localhost:5000/` to access the main page.
- Navigate to `/search` to search for meta decks.
- Navigate to `/war-decks` to generate and manage war decks.
- Use the `/update-meta-decks` endpoint to update the database with the latest meta decks.

## Endpoints

- `GET /`: Home page.
- `GET /search`: Search for meta decks.
- `POST /search/update-meta-decks`: Update the database with the latest meta decks.
- `GET /war-decks`: Generate and manage war decks.
- `GET /helpers/cards-by-rarity`: Fetch card data by rarity.
- `POST /helpers/generate-decks-json`: Export decks to a JSON file.
- `POST /helpers/generate-cards-json`: Export cards to a JSON file.
