// Copyright (c) 2022, Probase Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Billing Profile', {
	refresh: function(frm) {
		addCss()
		// add button to process bills
		frm.add_custom_button('Process Bills',()=>{
			frappe.set_route('bill-processing/new-bill-processing-1')

		}).addClass("primary bill-process-btn")
	},
	setup: function(frm) {},
	'doc_link':(frm)=>{
		getDocFields(frm)
	}
});

// function to get document Fields
function getDocFields(frm){
	frappe.call({
		method: 'probase_erp.billing.overrides.bill_processor.get_doc_fields',
		args: {get_doc_meta:frm.doc.doc_link},
		freeze: true,
		callback: (response) => {
			frm.set_df_property('field_id', 'options', response.message); 
			frm.refresh_field('field_id');
		},
		error: (r) => {
			frappe.show_alert('Failed to fetch fields!', 5)
		}
	})
}

function addCss(){
	$('.col-lg-2.layout-side-section').css({
		background:'#F1EFED',
		borderRadius:8,
		padding:10,
		boxShadow: 'rgba(0, 0, 0, 0.24) 0px 3px 8px'
	})
	$('.ellipsis.title-text').css({
		fontSize:13,padding:'5px 5px',
		minWIdth:'200px',
		background:'linear-gradient(80deg,#1388C3,#29A3E0)',
		color:'white',
		borderRadius:5
	})
}