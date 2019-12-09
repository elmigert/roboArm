#!/usr/bin/env bash
# stream video data from mp laptop wecam to remote desctop
# exit on error
set -e

username="mp"
customip=$1
port=$2
globalip=$3


echo "--- Connecting to mp laptop ${username}@${customip} at port ${port}, global ip: ${globalip}"
echo ""
# connect to mp laptop, start video server in terminal muktiplexer
ssh -t ${username}@${customip} -p ${port} << EOF
  tmux kill-server
  sleep 1
  tmux new-session -d -s mp "cvlc -vvv v4l2:///dev/video0 --sout '#standard{access=http,mux=ogg,dst=proxy51.rt3.io:34130}'"
EOF
# wait for stream to start
sleep 2

echo "--- Starting VLC"
# start receiver
vlc --network-caching 1000 https://proxy51.rt3.io:34130
trap ssh ${username}@${globalip}:${port} 'tmux kill-server' EXIT
