#!/usr/bin/env bash
# stream video data from mp laptop wecam to remote desctop
# exit on error
set -e
echo "--- Connecting to mp laptop"
echo ""

# connect to mp laptop, start video server in terminal muktiplexer
ssh -t mp@192.168.0.235 << EOF
  tmux kill-server
  sleep 1
  tmux new-session -d -s mp "cvlc v4l2:///dev/video0 --sout '#transcode{vcodec=mp4v,vb=2000,acodec=none}:rtp{sdp=rtsp://:8554/}'"
EOF
# wait for stream to start
sleep 2

echo "--- Starting VLC"
# start receiver
vlc --network-caching 1000 rtsp://192.168.0.235:8554/
trap ssh -t mp@192.168.0.235 'tmux kill-server' EXIT
