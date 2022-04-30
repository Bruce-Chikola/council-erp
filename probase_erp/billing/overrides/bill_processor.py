from dbm import ndbm
import profile
import frappe
from datetime import date, datetime
import datetime
from probase_erp.billing.overrides.conversions import calculate_monthly_due_date, create_date, create_date_string, increment_month, increment_day, increment_week, increment_year

from frappe.query_builder.utils import DocType
# function to get doctype chargable fields


@frappe.whitelist()
def get_doc_fields(**args):
    fieldlist = []
    docMeta = frappe.get_meta(args.get('get_doc_meta'))
    for field in docMeta.get("fields"):
        if field.fieldtype == 'Currency' or field.fieldtype == 'Float':
            fieldlist.append(field.fieldname)
    return fieldlist


# to get frequencies for billing period doctype
@frappe.whitelist()
def get_period_frequency(**args):
    return frappe.get_doc('Billing Profile', args.get('get_frequency'), fields=['frequency']).frequency

# to get field [bill type and bill frequency]


@frappe.whitelist()
def get_profile_dependand_fields(**args):
    return frappe.db.get_value('Billing Profile', args.get('billing_profile_name'), ['frequency', 'type'])

# function that starts the process of bill processing


@frappe.whitelist()
def process_bills(**args):
    return init_billing(args)

# function to initialize billing


def init_billing(args):
    if args.get('frequency').lower() == 'daily':
        return run_daily_bills(args)
    elif args.get('frequency').lower() == 'weekly':
        return run_weekly_bills(args)
    elif args.get('frequency').lower() == 'monthly':
        return run_monthly_bills(args)
    elif args.get('frequency').lower() == 'annually':
        return run_annually_bills(args)

# function to run daily bills


def run_daily_bills(args):
    # get billing process data
    mapped_data = {}    
    prop = get_billing_properties(args)
    profile = prop['profile']
    periods = prop['periods']
    startDate = create_date(periods.start_period)
    endDate = create_date(periods.end_period)
    currentDate = startDate    
    endDay = increment_day(currentDate)
    billables = get_billables(profile.doc_link, profile.field_id)    
    if billables == False:
        return f"No bills to be processed!"
    mapped_data = map_billables(billables, profile.field_id)    
    # a loop to create a bill for each period
    while currentDate <= endDate:
        for current in range(len(mapped_data)):
            mapped_data[current]['total_bill'] += mapped_data[current]['charge']
        currentDate = increment_day(currentDate)
        endDay = increment_day(currentDate)
        if currentDate >= endDate:
            create_bills(mapped_data, profile, startDate, endDate)
    return f"Daily Bills From { create_date_string(periods.start_period) } to { create_date_string(endDate) } Processed Successfully!"

# run weekly bills
def run_weekly_bills(args):
    # get billing process data
    mapped_data = {}    
    prop = get_billing_properties(args)
    profile = prop['profile']
    periods = prop['periods']    
    currentDate = create_date(periods.start_period)
    startDate = currentDate
    finalDate = create_date(periods.end_period)
    currentEnd = increment_week(currentDate)   
    billables = get_billables(profile.doc_link, profile.field_id)    
    if billables == False:
        return f"No bills to be processed!"
    mapped_data = map_billables(billables, profile.field_id)    
    # a loop to create a bill for each period
    while currentDate <= finalDate:
        for current in range(len(mapped_data)):
            mapped_data[current]['total_bill'] += mapped_data[current]['charge']
        currentDate = increment_week(currentDate)
        currentEnd = increment_week(currentDate)
        if currentDate >= finalDate:
            create_bills(mapped_data, profile, startDate, currentEnd)
    return f"Weekly Bills From { create_date_string(periods.start_period) } to { create_date_string(periods.end_period) } Processed Successfully!"


# to run monthly bills
def run_monthly_bills(args):
    mapped_data = {}
    # get billing process data
    prop = get_billing_properties(args)
    profile = prop['profile']
    periods = prop['periods']
    startDate = create_date(periods.start_month)
    endDate = create_date(periods.end_month)
    currentDate = startDate
    currentEnd = calculate_monthly_due_date(currentDate)
    billables = get_billables(profile.doc_link, profile.field_id)
    if billables == False:
        return f"No bills to be processed!"
    mapped_data = map_billables(billables, profile.field_id)
    while currentDate <= endDate:
        for current in range(len(mapped_data)):
            mapped_data[current]['total_bill'] += mapped_data[current]['charge']
        currentDate = currentEnd
        currentEnd = calculate_monthly_due_date(currentDate)
        if currentDate >= endDate:
            create_bills(mapped_data, profile, currentDate, currentEnd)
    return f"Monthly Bills From { create_date_string(startDate) } to { create_date_string(endDate) } Processed Successfully!"

# to run annual bills


def run_annually_bills(args):
    # get billing process data
    mapped_data = {}
    prop = get_billing_properties(args)
    profile = prop['profile']
    periods = prop['periods']
    startYear = periods.start_year
    endYear = create_date(periods.end_year)
    startDate = create_date(startYear)
    currentEnd = increment_year(startYear)
    currentDate = startDate
    billables = get_billables(profile.doc_link, profile.field_id)
    if billables == False:
        return f"No bills to be processed!"
    mapped_data = map_billables(billables, profile.field_id)
    # a loop to create a bill for each period
    while currentDate <= endYear:
        for current in range(len(mapped_data)):
            mapped_data[current]['total_bill'] += mapped_data[current]['charge']
        currentDate = increment_year(currentDate)
        currentEnd = increment_year(currentDate)
    if currentDate >= endYear:
            create_bills(mapped_data, profile, startYear, endYear)
    return f"Annual Bills From { create_date_string(startYear) } to { create_date_string(endYear) } Processed Successfully!"

# function to map billable docs to the billing charges array


def map_billables(billables, chargeableField):
    charges = []
    for billable in billables:
        charges.append(
            {'name': billable.name, 'charge': billable[chargeableField], 'total_bill': 0})
    return charges


# function to finally create bill
def create_bills(mapped_data, profile, startDate, compDate):
    for doc in mapped_data:        
        last_bill = calc_last_bill(doc, profile)             
        if frappe.db.count("Bills", {'doc_id': doc['name'], 'date_created': startDate, 'due_date': compDate}) == 0:
            new_bill = frappe.new_doc('Bills')
            new_bill.date_created = startDate
            new_bill.due_date = compDate
            new_bill.total_bill = last_bill['total_bill']
            new_bill.balance_bf = last_bill['bal_bf']
            new_bill.balance_cd = last_bill['bal_cd']
            new_bill.paid = last_bill['paid']
            new_bill.doctype_name = profile.doc_link
            new_bill.doc_id = doc['name']
            new_bill.charge = doc['charge']
            new_bill.description = profile.type
            new_bill.frequency = profile.frequency
            new_bill.processor_reference = doc['name']
            new_bill.save()
            create_invoice(profile)
            frappe.db.commit()
    return True



# function to calculate last bill figures
def calc_last_bill(doc, profile):
    bal_bf = 0
    bal_cd = 0
    total_bill = doc['total_bill']
    paid = 0
    
    last_bill = get_last_biill_charge(doc)
    if last_bill != False:
        if last_bill.paid > 0:
            if last_bill.balance_cd > 0:
                bal_bf = last_bill.balance_cd
                total_bill = bal_bf + doc['charge']
                bal_cd = total_bill
            elif last_bill.balance_cd < 0:
                bal_bf = last_bill.balance_cd
                if((bal_bf * -1) > doc['charge']):
                    total_bill = doc['charge']
                    paid = total_bill
                    bal_cd = (bal_bf + paid)
                else:
                    total_bill = (bal_bf + doc['charge'])
                    paid = bal_bf * -1
                    bal_cd = total_bill
        elif last_bill.paid == 0:
            total_bill = last_bill.total_bill + doc['charge']
            bal_bf = last_bill.balance_cd
            bal_cd = total_bill
    else:
        bal_cd = total_bill
    # frappe.throw(f"{doc}")  
    return {'bal_bf': bal_bf, 'bal_cd': bal_cd, 'total_bill': total_bill, 'paid': paid}


# function to get the last bill charges
def get_last_biill_charge(doc):
    if frappe.db.exists('Bills', {'doc_id': doc['name']}):
        return frappe.get_last_doc('Bills', {'doc_id': doc['name']})
    return False

# function to get billing periods and profile
def get_billing_properties(args):
    return {
        'process': frappe.get_doc('Bill Processing', args.get('doc_name')),
        'periods': frappe.get_doc('Billing Period', args.get('billing_period')),
        'profile': frappe.get_doc('Billing Profile', args.get('billing_profile'))
    }


# function to get billables for the doctype
def get_billables(docType, chargeField):
    billables = frappe.get_all(
        docType, fields=['name', chargeField], order_by='creation')
    if len(billables) > 0:
        return billables
    return False

    # Function to create Sales Invoices for each new bill


def create_invoice(bill_profile):
    # defining the relevant varaibles that will be used to fill Sales Invoice Form
    bill = frappe.get_last_doc('Bills')
    company = frappe.db.get_default("Company")
    currency = frappe.db.get_default("currency")
    today = date.today()
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    doc_id = bill.doc_id
    bill_id = bill.name
    charge_amount = float(bill.total_bill)
    processor_ref = bill.processor_reference
    bill_desc = bill.description
    # defining an "item name" variable that matches the relevant item object that will be inserted into invoice form
    item_naming = str(bill_profile.doc_link) + " " + str(bill_profile.frequency) + " " + str(bill_profile.type)
    doc_obj = frappe.get_doc(bill_profile.doc_link, doc_id)
    customer = doc_obj.customer
    customer_obj = frappe.get_doc('Customer', customer)
    bill_obj = frappe.get_doc('Bills', bill_id)
    # setting the item object to 'enabled'
    item_obj = frappe.get_doc('Item', item_naming)
    item_obj.db_set('disabled', 0)

    # automatic Sales Invoice form filling
    doc = frappe.get_doc(
        {
            'doctype': 'Sales Invoice',
            "docstatus": 1,
            "naming_series": "Bill-.##.-" + doc_id + "-.YYYY.-",
            "company": company,
            "posting_date": today,
            "currency": currency,
            "price_list_currency": currency,
            "items": [
                {
                    "docstatus": 1,
                    "doctype": "Sales Invoice Item",
                    "stock_uom": None,
                    "cost_center": "Main - pbs",
                    "parentfield": "items",
                    "parenttype": "Sales Invoice",
                    "idx": 1,
                    "qty": 1,
                    "conversion_factor": 1,
                    "stock_qty": 1,
                    "price_list_rate": charge_amount,
                    "base_price_list_rate": charge_amount,
                    "rate": charge_amount,
                    "amount": charge_amount,
                    "base_rate": charge_amount,
                    "base_amount": charge_amount,
                    "stock_uom_rate": charge_amount,
                    "net_rate": charge_amount,
                    "net_amount": charge_amount,
                    "base_net_rate": charge_amount,
                    "base_net_amount": charge_amount,
                    "item_code": item_naming,
                    "weight_uom": 0,
                    "item_name": processor_ref,
                    "description": bill_desc,
                    "warehouse": "Stores - pbs",
                    "income_account": "Sales - pbs",
                    "expense_account": "Cost of Goods Sold - pbs",
                    "transaction_date": today,
                }
            ],
            "posting_time": time,
            "conversion_rate": 1,
            "plc_conversion_rate": 1,
            "debit_to": "Debtors - pbs",
            "base_net_total": charge_amount,
            "net_total": charge_amount,
            "base_total": charge_amount,
            "total": charge_amount,
            "total_qty": 1,
            "rounding_adjustment": -charge_amount,
            "grand_total": charge_amount,
            "base_grand_total": charge_amount,
            "due_date": today,
            "customer": customer,
            "language": "en-US",
            "bill_tied_to": bill_id,
        }
    )
    # inserting the form into the database
    doc.insert()
    frappe.db.commit()
    # getting the sales invoice object we just inserted
    last_invoice = frappe.get_last_doc('Sales Invoice')
    # updating the "attache invoice " field of the bill
    bill_obj.attached_invoice = last_invoice.name
    bill_obj.save()
# to process bills pano.
