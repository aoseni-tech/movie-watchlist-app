#!/bin/bash

cd /home/ec2-user/movie_watchlist_app/

export AWS_MOVIEWATCHLIST_CONFIG="$(aws secretsmanager get-secret-value --secret-id movie_watchlist_env)"

nohup web: gunicorn "movie_watchlist:create_app()" > my.log 2>&1 &
echo $! > save_pid.txt