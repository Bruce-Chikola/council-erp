# Copyright (c) 2022, Probase Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BillingProfile(Document):
    def before_save(self):

        # definition of relevanr variables to be used in filling of Item form
        company = frappe.db.get_default("Company")
        store = frappe.db.get_default("default_warehouse")

        # defining an "item name" variable that will match the item name variable defined in invoice creation
        item_naming = str(self.doc_link) + " " + str(self.frequency) + " " + str(self.type)

        # only create a new item if it doesn't exit
        if frappe.db.exists("Item", item_naming, cache=True) == None:
            # Automatic filling of Item form
            doc = frappe.get_doc(
                {
                    "name": item_naming,
                    "owner": "Administrator",
                    "docstatus": 0,
                    "naming_series": "Bill-.YYYY.-",
                    "item_code": item_naming,
                    "item_name": item_naming,
                    "item_group": "Products",
                    "stock_uom": "Nos",
                    "disabled": 1,
                    "allow_alternative_item": 0,
                    "is_stock_item": 0,
                    "include_item_in_manufacturing": 0,
                    "opening_stock": 0,
                    "valuation_rate": 0,
                    "standard_rate": 0,
                    "is_property_idfixed_asset": 0,
                    "auto_create_assets": 0,
                    "over_delivery_receipt_allowance": 0,
                    "over_billing_allowance": 0,
                    "description": 'temp',
                    "shelf_life_in_days": 0,
                    "end_of_life": "2099-12-31",
                    "default_material_request_type": "Purchase",
                    "valuation_method": "",
                    "weight_per_unit": 0,
                    "has_batch_no": 0,
                    "create_new_batch": 0,
                    "has_expiry_date": 0,
                    "retain_sample": 0,
                    "sample_quantity": 0,
                    "has_serial_no": 0,
                    "has_variants": 0,
                    "variant_based_on": "Item Attribute",
                    "is_purchase_item": 1,
                    "min_order_qty": 0,
                    "safety_stock": 0,
                    "lead_time_days": 0,
                    "last_purchase_rate": 0,
                    "is_customer_provided_item": 0,
                    "delivered_by_supplier": 0,
                    "country_of_origin": "Zambia",
                    "is_sales_item": 1,
                    "grant_commission": 1,
                    "max_discount": 0,
                    "enable_deferred_revenue": 0,
                    "no_of_months": 0,
                    "enable_deferred_expense": 0,
                    "no_of_months_exp": 0,
                    "inspection_required_before_purchase": 0,
                    "inspection_required_before_delivery": 0,
                    "is_sub_contracted_item": 0,
                    "customer_code": "01",
                    "show_in_website": 0,
                    "show_variant_in_website": 0,
                    "weightage": 0,
                    "total_projected_qty": 0,
                    "doctype": "Item",
                    "barcodes": [],
                    "reorder_levels": [],
                    "uoms": [
                        {
                            "name": "99f7d56dbf",
                                    "creation": "2022-01-18 11:36:25.749340",
                            "modified": "2022-01-18 11:36:25.749340",
                            "modified_by": "Administrator",
                            "parent": "110550",
                            "parentfield": "uoms",
                            "parenttype": "Item",
                            "idx": 1,
                            "docstatus": 0,
                            "uom": "Nos",
                            "conversion_factor": 1,
                            "doctype": "UOM Conversion Detail"
                        }
                    ],
                    "attributes": [],
                    "item_defaults": [
                        {
                            "parent": item_naming,
                            "parentfield": "item_defaults",
                            "parenttype": "Item",
                            "idx": 1,
                            "docstatus": 0,
                            "company": company,
                            "default_warehouse": store,
                            "doctype": "Item Default"
                        }
                    ],
                }
            )
            # inserting the the filled form into the database
            doc.insert()
            print(doc)
            frappe.db.commit()
       