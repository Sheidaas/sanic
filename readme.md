This is **undetected web scrawler**

Here you could:
 - easy describe models of business data
 - undetected scrap business data from web services

*Connecting*

To connect from web servers to access database and processes check out *open_api.yaml*

*Sections*

Each section is a different element of docker compose configuration.

*Database* - postgres

*nginx* - reverse proxy

*webserver/backend* - see more in server.readme.md

*Launching*

Aby uruchomić projekt należy użyć komendy **docker compose up** mając
zainstalowanego dockera oraz dockera-compose. 

*Logger Configuration* 

Settings of filenames and access levels are in *resources/config.ini*
For more look into *server.src.utils.logger*
