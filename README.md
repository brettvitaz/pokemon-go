# Pokémon Go Registry

Application and services for a Pokémon Go Registry.

The purpose of this application is to provide a place for players to register their seen and caught pokémon so that they can get useful information about their quality and evolution potential. Player data will be analyzed to identify trends and create interactive charts and maps.

Goals:
- Multi-player login
- Store player data
    + Eggs
    + Items
    + Experience
    + Candies
    + Favorite gym (location)
- Store seen and caught pokémon
    + Type
    + Basic stats
    + Attacks
    + Location
    + Battles won/lost
- Provide analytics, charts, and maps for 
    + Pokémon quality and evolution potential
    + Pokémon battle statistics
    + Pokémon spawn locations

Proposed stack:
- PostgreSQL Database
- Python API
    + Flask
    + SQLAlchemy
    + Marshmallow
- Node/Express Front End
    + D3
    + React
    + Redux
- Docker
