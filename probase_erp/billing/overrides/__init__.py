import frappe
import json
from frappe import _
from pprint import pprint
from dataclasses import fields
from datetime import date
import datetime
def on_save(doc, status):
    pass

def on_payment(doc, status):
    # code for updating an existing bill for which a payment has been made    
    payment_obj = frappe.get_last_doc('Payment Entry')
    for ref in payment_obj.references:       
       ref_name = frappe.db.get_value('Payment Entry Reference', ref.name, 'reference_name')
       break
    invoice_obj = frappe.get_doc('Sales Invoice', ref_name)    
    bill_name = invoice_obj.bill_tied_to
    paid = payment_obj.paid_amount
    outstanding_amount = invoice_obj.outstanding_amount
    unallocated_amount = payment_obj.unallocated_amount

    doc = frappe.get_doc('Bills', bill_name)
    doc.balance_cd = outstanding_amount - unallocated_amount
    doc.paid = paid
    
    doc.save()
        
    
    
        