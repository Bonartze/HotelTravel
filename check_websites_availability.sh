#!/bin/bash

# Array of websites to check
websites=("https://www.booking.com" "https://www.atlasobscura.com")

# Loop through the list of websites
for site in "${websites[@]}"; do
  # Send a request and check if the response code is 200 (OK)
  if curl -Is "$site" | head -n 1 | grep "200 OK" > /dev/null
  then
    echo "Website $site is available."
  else
    echo "Website $site is not available."
  fi
done
