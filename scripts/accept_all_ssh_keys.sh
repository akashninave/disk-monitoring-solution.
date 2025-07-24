#!/bin/bash

USER="akashninave"   # Replace with your actual Mac username

IPS=(
  10.0.1.1 10.0.1.2 10.0.1.3
  10.1.1.1 10.1.1.2 10.1.1.3 10.1.1.4
  10.2.1.1 10.2.1.2 10.2.1.3 10.2.1.4 10.2.1.5
  10.3.1.1 10.3.1.2 10.3.1.3
  10.4.1.1 10.4.1.2 10.4.1.3 10.4.1.4
  10.5.1.1 10.5.1.2 10.5.1.3 10.5.1.4 10.5.1.5 10.5.1.6
  10.6.1.1 10.6.1.2 10.6.1.3 10.6.1.4
  10.7.1.1 10.7.1.2 10.7.1.3 10.7.1.4 10.7.1.5 10.7.1.6 10.7.1.7
  10.8.1.1 10.8.1.2 10.8.1.3
)

for ip in "${IPS[@]}"
do
  echo "Connecting to $ip..."
  ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 $USER@$ip exit
done

echo "All done!"
