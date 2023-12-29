#!/bin/bash

cd /home/ec2-user/movie_watchlist_app/

kill `cat save_pid.txt`
rm save_pid.txt