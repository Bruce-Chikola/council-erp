# Copyright (c) 2022, Probase Limited and contributors
# For license information, please see license.txt
import frappe
from frappe.model.naming import make_autoname
# import frappe
from frappe.model.document import Document

class Bills(Document):
    	pass
	# def before_save(self):
	# 	self.name = 'Bill-'+self.doc_id +' - '+ self.date_created.strftime("%Y/%m/%d") + '  - To -'+ self.due_date.strftime("%Y/%m/%d")  + make_autoname(' -.#####')