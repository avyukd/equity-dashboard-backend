# Equity Dashboard

A personal dashboard to help me keep track of my investments. Built with FastAPI and React. Frontend here: https://github.com/avyukd/equity-dashboard. 

To run locally: 
- frontend: yarn start
- backend: uvicorn main:app

## Motivation

A lot of my personal investment research (valuations, company notes, portfolio size, charts, etc.) was disorganized and hard to find and manage. To solve this problem, I'm building the Equity Dashboard, a centralized platform that helps me manage my investments. 

## Features
- Semantic search over bookmarked investment research (using OpenAI GPT-3)
- Dashboards for various investment themes. Each dashboard includes a number of equities which are updated daily against their valuations from the backend
- General market indicators updated daily (shiller PE, margin debt YOY, fear/greed index, SP500/DOW/NASDAQ movement)
- Commodities supply/demand model (currently only for Uranium)
- Watchlist (currently stored in SQLite, migrating to MongoDB)

### Working on adding...
- Functioning cache
- Note taking space for individual equities (using Draft.js)
- Auto-updated bookmarking (using chrome extension)
- More investment themes and supply/demand models (oil, china tech) 
- Sign-in + deployment to share with others

## Walk-through

Watchlist: 
![image](https://user-images.githubusercontent.com/25803234/131032256-e671eb41-d14e-4656-b316-cf6b1275cab6.png)

General indicators:
![image](https://user-images.githubusercontent.com/25803234/131032305-5a222a82-3081-4040-89a7-2330a2844fea.png)

Semantic search over bookmarks:
![image](https://user-images.githubusercontent.com/25803234/131032580-158c41a3-7a94-49ee-8c5e-19022726a912.png)
- Searches full-text of links
- Search based on meaning, not keyword (for example: search for canine, still get results with just dog in them)

Commodities Dashboard (Uranium):
At current prices:
![image](https://user-images.githubusercontent.com/25803234/131032761-a29cc11a-1b7d-4e25-a298-20fe051677b4.png)

At higher prices:
![image](https://user-images.githubusercontent.com/25803234/131032836-4be3eb78-7aff-4722-83a3-0109326fb874.png)

Supply/Demand Model (Uranium):
![image](https://user-images.githubusercontent.com/25803234/131033000-10fbcc83-9462-48ec-b4be-82bb3439695c.png)
- Can change inputs to see impact on S/D

Other Dashboards:
![image](https://user-images.githubusercontent.com/25803234/131033078-2e7a7dbe-ba6e-48b2-a7bb-d0aafce854cc.png)

Note-taking for individual equities:
![image](https://user-images.githubusercontent.com/25803234/131033163-b721f786-189a-477d-ae99-21f51afbe8f2.png)

