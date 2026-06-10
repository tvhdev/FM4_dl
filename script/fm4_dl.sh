#!/usr/bin/env bash
cd "$(dirname "$0")" #set wd to file location
SHOW_TAGS=(4D1 4TV 4GP 4UL 4DKM 4DD 4LB 4SS 4DLL)  #insert you favourite show tags here
STORAGE=/mnt/storage/Musik/FM4/downloads
for SHOW_TAG in "${SHOW_TAGS[@]}"; do
  mkdir -p ${STORAGE}/${SHOW_TAG} #creates show directory if it doesn't exist
  #call python script to get date/url of every available broadcast (up to 4 weeks back)
  while read -r DATE PART_IDX PART_TOTAL URL; do
    [ -z "${URL}" ] && continue #skip empty lines
    if [ "${PART_TOTAL}" -gt 1 ]
    then
      FILENAME="${STORAGE}/${SHOW_TAG}/${DATE}_${SHOW_TAG}_${PART_IDX}.mp3"
    else
      FILENAME="${STORAGE}/${SHOW_TAG}/${DATE}_${SHOW_TAG}.mp3"
    fi
    PARTFILE="${FILENAME}.part"
    if [ ! -f ${FILENAME} ]
    then
      logger "downloading ${FILENAME}"
      if wget -c -O ${PARTFILE} ${URL} #download show, resume if a previous attempt was interrupted
      then
        mv ${PARTFILE} ${FILENAME}
        #upload to cloud? use rclone!
      else
        logger "download of ${FILENAME} failed/incomplete, will resume on next run"
      fi
    else
      logger "skipping file ${FILENAME}, it does already exist"
    fi
  done < <(python fm4.py -s ${SHOW_TAG} --all)
done
