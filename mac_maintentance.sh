## Commands for system maintenance
## Run in this order (uncomment last line if restarting computer)

# purge RAM and other purgable space
echo "purging RAM and clearing purgable space"
sudo purge;
echo "Done"
echo "___________________________"


# check last maintenance
echo "Before running this file, maintenance scripts were last run:"
ls -al /var/log/*.out
# run maintenance scripts
echo "___________________________"
echo "Running maintenance scritps..."
sudo periodic daily weekly monthly
# check last maintenance
echo "___________________________"
echo "Updated Maintenance script log:"
ls -al /var/log/*.out
echo "Done"
echo "___________________________"


# purge DNS/UDNS
echo "Flushing DNS and UDNS cahces..."
sudo dscacheutil -flushcache; 
sudo killall -HUP mDNSResponder;
echo "Done"
echo "___________________________"


# reset/rebuild launch services
echo "Rebuilding launch services..."
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
echo "Done"
echo "___________________________"

# purge RAM and other purgable space
echo 'purging RAM and clearing purgable space'
sudo purge;
echo "Done"
echo "___________________________"

# update and restart
echo 'updating ...'
sudo softwareupdate -iaR
echo "Done"
echo "___________________________"


# clear NVRAM before restart/poweroff
echo 'Clearing NVRAM…'
sudo nvram -c
echo ‘NVRAM’ 
sudo shutdown -h now
