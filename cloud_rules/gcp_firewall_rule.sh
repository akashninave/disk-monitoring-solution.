#!/bin/bash

gcloud compute firewall-rules create allow-ansible-ssh \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=10.0.0.10/32 \
  --description="Allow SSH from Ansible VM"
