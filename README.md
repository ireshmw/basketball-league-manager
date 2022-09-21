# Basketball-League-Manager


## Project setup instuctions

01) To run the project (start the server) use the following command
```
py manage.py runserver
```

02) To add dummy data to the db ( here i included the SQLite DB file as well if you need fresh dummy data you can use fixture file,  file location - data/fixtures/game-data.json )
```
py manage.py loaddata game-data.json
```


## API endpoints 


### Scoreboard 

all the game details in tree structure (GameRound->games->tems)  
http://localhost:8000/api/v1/dashboard

get all the game details for the scoreboard
include games and teams of the particular game with their scores.  
http://127.0.0.1:8000/api/v1/games      



### Coach

get a team of the coach, here path variable is coach-id  (include hyperlinks to player list of the team)  
http://localhost:8000/api/v1/coach-team/3/  

get payer list of the coach, here path variable is coach-id  
http://localhost:8000/api/v1/coach-players/1/  

full details of the player, here path variable is player-id  
http://localhost:8000/api/v1/player/1/

Get Above 90 Percentile Players Of Coach, here path variable is coach-id  
http://localhost:8000/api/v1/coach-players-above-avg/3/



### League admin

view all the team (include hyperlinks to player list of the team)  
http://localhost:8000/api/v1/teams/

## ER Diagram

![alt text](https://github.com/ireshmw/basketball-league-manager/blob/master/data_game.png)





