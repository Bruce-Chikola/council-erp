import frappe
from frappe import _
from frappe.model.document import Document

class PaymentEntry(Document):

    def on_save(doc):
        frappe.throw(_("We're here"))