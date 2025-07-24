#!/bin/bash
# Sample Input: No arguments needed; run on the VM itself

USER_NAME=$(whoami)
output_file_txt="storage_info_${USER_NAME}_$(date +%F).txt"
output_file_csv="storage_info_${USER_NAME}_$(date +%F).csv"

# Original detailed text output
{
  echo "===== Disk Usage (df -h) ====="
  df -h

  echo -e "\n===== Block Devices (lsblk) ====="
  lsblk

  echo -e "\n===== Disk Usage Summary (du -sh /*) ====="
  du -sh /* 2>/dev/null

  echo -e "\n===== Mounted Filesystems ====="
  mount | column -t

  echo -e "\n===== Inode Usage (df -i) ====="
  df -i
} > "$output_file_txt"

echo "Storage info saved to $output_file_txt"

# CSV output header
echo "Filesystem,Size,Used,Available,Use%,MountedOn" > "$output_file_csv"

# CSV data from df
df -h --output=source,size,used,avail,pcent,target | tail -n +2 | \
  awk '{print $1","$2","$3","$4","$5","$6}' >> "$output_file_csv"

echo "Storage CSV info saved to $output_file_csv"
