
def schedule_periodic(scheduler, interval, action, actionargs={}, wait=False):
	def periodic():
		scheduler.enter(interval, 1, periodic)
		action(*actionargs)
	if wait is True:
		first_time = interval
	else:
		first_time = 1
	scheduler.enter(first_time, 1, periodic)
