# Path of Exile Currency Tracker

A self-hosted data pipeline for tracking **Path of Exile 2** currency exchange rates in real-time, 
built as a personal project using Python, Docker, PostgreSQL, and data automation.

# Overview

The idea was to create a pipeline that fetches live currency exchange data from the poe.ninja API every 30 minutes, then stores it in a PostgreSQL database, and visualises price trends on a Grafana dashboard. The entire build runs on a self-hosted Hetzner VPS in Docker containers. It was built as a portfolio piece to demonstrate junior sysadmin and DevOps skills:
- server provisioning
- containerisation
- database design 
- monitoring dashboards
- CI/CD pipelines


## Architecture

The project has 3 components running as Docker Containers using Docker Compose:

| Service |  Image | Port | Purpose |
|--|--|--|--|
| fetcher | custom | N/A | Fetches API data, writes to DB every 30 min |
| database |  postgres:16 | 5432 | Stores all historical price snapshots |
| grafana | grafana | 3000 | Live dashboard, publicly accessible |

> Thanks to Docker Compose all services share an internal Docker network.

   **Project Diagram**
   
    poe.ninja API
		  |
	  [fetcher] --writes--> [PostgreSQL db]
								   |
							   [Grafana] --> browser

## Prerequisites

A Linux VPS, this project is uses **Ubuntu 24.04** on **Hetzner CX22** 
**Docker** and **Docker Compose** plugin installed
**Git** installed on the server
Ports **22, 80, 443, 3000** open in UFW
SSH Key Authorisation?
Editing YAML files with their own credentials?

## Quick Start

Clone the repository and set up your .env file:

    git clone https://github.com/yourusername/poe-economy-tracker.git
    cd poe-economy-tracker
    nano .env
  
Open .env and fill in with your database credentials:

    POSTGRES_DB=poedb
    POSTGRES_USER=poeuser
    POSTGRES_PASSWORD=yourpassword

Start it as a Docker:

    docker compose up -d
    
or

    docker compose -f custom_name_of_your_yaml_file.yaml up

**Grafana** will be available at http://your-server-ip:3000 within a few seconds. 
Default login is admin/admin and changing it is recommended .
> The fetcher runs its first data pull immediately on startup, then every 30 minutes

## Environment Variables

| Variable |  Example | Description 
|--|--|--|
| POSTGRES_DB | poedb | Name of your PostgreSQL database 
| POSTGRES_USER |  admin | Database Username
| POSTGRES_PASSWORD | admin | Database Password
| GRAFANA_PORT | 3000 | Port the Grafana will be accessable at

## Live Dashboard

The Grafana dashboard is publicly accessible at:
http://178.105.59.4:3000 or 
your_VPS_IP:grafana_port

**The dashboard includes the following panels:**
-   Currency value over time - single currency line chart with 30-minute resolution
-   Multi-currency comparison - compare up to all currencies on one chart
-   Current snapshot table - the most recent fetch, showing all currencies and their current values
-   Mirror of Kalandra stat panel - current price of the most valuable currency as a large number with colour thresholds

## Skills Demonstrated

| # |  Skills | What this project demonstrates | 
|--|--|--|
| 1 | Linux CLI | Provisioned and hardened a Hetzner VPS: UFW, SSH keys, non-root user, auto-updates |
| 2 |  Docker & Compose | Three-service stack with volumes, healthchecks, internal networking, and restart policies |
| 3 | Python Scripting | API fetching, JSON parsing, psycopg2 database writes, error handling, scheduling |
| 4 | PostgreSQL | Schema design, appropriate data types, indexing for time-series queries, parameterised inserts |
| 5 |  Grafana | PostgreSQL data source, time-series panels, dashboard variables, JSON export |
| 6 | CI/CD | GitHub Actions workflow: test job, deploy job, SSH deployment, secrets management |
| 7 | Documentation | README quick-start, architecture diagram, runbook for operational procedures |

## Repository Structure

    poe-economy-tracker/
	    fetcher/
		    main.py
		    poe_fetcher.py
		    poe_database.py
		    Dockerfile
		    requirements.txt
		 grafana/
			dashboard.json
		.github/workflows/
			 deploy.yml
		 docker-compose.yml
		 .env
		 README.md
		 RUNBOOK.md
		   

## Data Source

Currency data is fetched from the poe.ninja public API:

    https://poe.ninja/poe2/api/economy/exchange/current/overview?league=Fate+of+the+Vaal&type=Currency

No API key is required. The fetcher respects a 30-minute interval to avoid hitting any rate limits. If the API is unavailable, the fetcher logs the error and waits for the next scheduled run — no data is lost, the gap simply won't appear in the charts.
