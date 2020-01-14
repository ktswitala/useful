
try:
	import wmi
	w = wmi.WMI()
	def find_local_volumes(**kwargs):
		volumes = w.Win32_Volume(**kwargs)
		return volumes

	def find_logical_disks(**kwargs):
		logicaldisks = w.Win32_LogicalDisk(**kwargs)
		return logicaldisks

	def find_physical_disks(logical_disk):
		partitions = logical_disk.associators(wmi_association_class='Win32_LogicalDiskToPartition')
		disks = []
		for partition in partitions:
			disks += partition.associators(wmi_association_class='Win32_DiskDriveToDiskPartition')
		disk_serials = [d.SerialNumber for d in disks]
		return disk_serials

	def find_root_dir(logical_disk):
		try:
			root_dirs = logical_disk.associators(wmi_association_class='Win32_LogicalDiskRootDirectory')
		except wmi.x_wmi as x:
			print("com error", x)
			return None
		return list(map(lambda d: d.Name, root_dirs))[0]
except:
	pass
