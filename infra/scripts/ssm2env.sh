#!/bin/bash
cd /home/ubuntu/groovy-api
if [ -f ".env" ] ; then
  rm .env
fi
aws ssm get-parameters-by-path \
  --path "/groovy-api/" \
  --with-decryption \
  --query "Parameters[*].[Name,Value]" \
  --output text |
  while read line
  do
    name=$(echo ${line} | cut -f 1 -d ' ' | sed -e 's/\/groovy-api\///g')
    value=$(echo ${line} | cut -f 2 -d ' ')
    echo "${name}=${value}" >> .env
  done
