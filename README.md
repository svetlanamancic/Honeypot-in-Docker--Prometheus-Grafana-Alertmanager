# Docker Honeypot and Monitoring with Prometheus, Alertmanager & Grafana

## Prometheus Targets & Alerts

![image](https://github.com/user-attachments/assets/0a2be7d9-cf8d-4ff9-a3f5-abc2aab09e14)

![image](https://github.com/user-attachments/assets/c84bf074-9359-4753-af8f-067c7bb8dbb2)

## Grafana Dashboard

![image](https://github.com/user-attachments/assets/b35207b5-2fce-4644-b4a9-a5b0288ad761)

## Telegram Alerts

<p align="center" width="100%">
  <img width="40%" src="https://github.com/user-attachments/assets/abff6f2b-20cb-40a5-a822-4bfc496ff4a6"/>
</p>



## Services

`ssh-honeypot` service contains modified openssh package and prometheus exporter which monitors ssh logs and exports metrics.

`prometheus` service contains prometheus server which scrapes metrics from the honeypot and evaluates the metrics for alerts.

`alertmanager` service contains alertmanager component which receives alerts from prometheus and sends them to Telegram channel.

`grafana` service contains grafana server with predefined dashboard for honeypot metrics monitoring, which is pulled from prometheus.

## Build

First make sure ports 22, 3000, 8000, 9090, 9093 are available so the containers can be started. 

Bot token is ommited in this repository. To receive alerts create and configure new bot ( [Telegram Bots Docs](https://core.telegram.org/bots/tutorial) ) -- also, check alertmanager.yaml file to learn how to pass bot token.

To build and spin up containers navigate to the root folder containing `docker-compose.yml` file and execute:

```bash
> make up
```

Inside Docker `prometheus` runs on http://localhost:9090

Inside Docker `alertmanager` runs on http://localhost:9093

Inside Docker `grafana` runs on http://localhost:3000

Inside Docker `ssh-honeypot` runs on 0.0.0.0:22


