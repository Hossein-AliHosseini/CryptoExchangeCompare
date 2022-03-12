#!/bin/bash

echo "Starting CryptoExchangeCompare Project..."

sudo docker-compose build &&
  sudo docker-compose up --remove-orphans