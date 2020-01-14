
import selenium.webdriver
import selenium.common

def count_frames(driver):
	i = 0
	try:
		while i < 10:
			driver.switch_to.frame(i)
			i += 1
	except:
		pass
	return i

class PageMonitor(object):
	def __init__(self, driver, page_update_cb):
		self.driver = driver
		self.page_update_cb = page_update_cb
		self.currentURLs = {}
		self.currentWindows = []

	def update(self):
		if self.driver.window_handles != self.currentWindows:
			for window in self.driver.window_handles:
				if window not in self.currentWindows:
					self.driver.switch_to.window(window)
					self.currentURLs[window] = self.driver.current_url
					self.page_update_cb(self.driver.current_url, self.driver.page_source)
			self.currentWindows = self.driver.window_handles
		if self.driver.current_url != self.currentURLs[self.driver.current_window_handle]:
			self.currentURLs[self.driver.current_window_handle] = self.driver.current_url
			self.page_update_cb(self.driver.current_url, self.driver.page_source)
