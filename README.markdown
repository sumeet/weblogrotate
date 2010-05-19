# Web log rotator, built for jwoww.system573.org

Run this in crontab, with something like this:
	0 5 * * * rotateweb.py && apache2ctl graceful;/etc/init.d/cherokee reload

