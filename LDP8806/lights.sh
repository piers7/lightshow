#! /bin/sh
# /etc/init.d/lights

### BEGIN INIT INFO
# Provides: lightshow
# Required-Start: $remote_fs$ $syslog$
# Required-Stop: $remote_fs$ $syslog$
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: runs light show on startup
# Description: Runs lightshow on startup
### END INIT INFO

HOME=/home/pi
USER=pi
SCRIPT_DIR=/home/pi/dev/lightstrip/LDP8806
SCRIPT_NAME=lightshow.py

case "$1" in
	start)
		echo "Starting lights"
		#python /home/pi/ws281x/arches.py 120 2 &
                #python /home/pi/dev/lightstrip/LDP8806/lightshow.py &
		echo "Starting $SCRIPT_DIR/$SCRIPT_NAME" > $SCRIPT_DIR/log.log
		su 'root' -c "python $SCRIPT_DIR/$SCRIPT_NAME >> $SCRIPT_DIR/log.log &"
		;;
	stop)
		echo "Stopping lights"
		killall python
		;;
	*)
		echo "Usage /etc/init.d/lights start|stop"
		exit 1
		;;
esac
exit 0
