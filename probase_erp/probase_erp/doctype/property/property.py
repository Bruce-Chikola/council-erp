# Copyright (c) 2021, Probase Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date
import datetime, calendar

from frappe.utils.data import add_months


class Property(Document):
    def before_save(self):
        self.property_account_no = self.name

    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)
