from concurrent.futures import thread
from datetime import datetime
from unittest.mock import seal
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from probase_erp.billing.overrides.conversions import calculate_monthly_due_date, create_date, create_date_from_object, create_date_string, increment_month, increment_day, increment_week, increment_year


class BillingPeriod(Document):		
	def before_save(self):
			
		if self.formatter == 'daily':
				self.name = 'Daily ' +create_date_string(create_date_from_object(self.start_period))+'  To  '+ create_date_string(create_date_from_object(self.end_period)) + make_autoname(' -.#####')
		if self.formatter == 'weekly':
				self.name = 'Weekly ' + create_date_string(create_date_from_object(self.start_period))+'  To  '+ create_date_string(create_date_from_object(self.end_period)) + make_autoname(' -.#####')	
		elif self.formatter == 'monthly':
				self.name = 'Monthly From ' +create_date_string(create_date_from_object(self.start_month))+'  To  '+ create_date_string(create_date_from_object(self.end_month)) + make_autoname(' -.#####')
		elif self.formatter == 'annually':
				self.name = 'Anually ' +create_date_string(create_date_from_object(self.start_year))+'  To  '+ create_date_string(create_date_from_object(self.end_year)) + make_autoname(' -.#####')
		
