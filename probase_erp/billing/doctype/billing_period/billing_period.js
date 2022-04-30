// Copyright (c) 2022, probase and contributors
// For license information, please see license.txt
frappe.ui.form.on('Billing Period', {
	refresh: function(frm) {
		addCss()
		cur_frm.set_df_property("billing_daily", "hidden", 1)
		cur_frm.set_df_property("biiling_monthly", "hidden", 1)
		cur_frm.set_df_property("billing_yearly", "hidden", 1)
		if(frm.doc.billing_profile) get_billing_frequency(frm)
	},
	'billing_profile':function(frm){
		if(frm.doc.billing_profile)  get_billing_frequency(frm)
	}
});

// function to get billing frequncy
function get_billing_frequency(frm){
	frappe.call({
		method: 'probase_erp.billing.overrides.bill_processor.get_period_frequency',
		args: {get_frequency:frm.doc.billing_profile},
		freeze: true,
		callback: (r) => {
			switch (r.message.toLowerCase().trim()) {
				case 'daily':
					cur_frm.set_value('formatter', "daily");
					switch_show_hide_period_sections('billing_daily')
					break;
				case 'weekly':
					cur_frm.set_value('formatter', "weekly");
					switch_show_hide_period_sections('billing_daily')
					break;
				case 'monthly':
					cur_frm.set_value('formatter', "monthly");
					switch_show_hide_period_sections('biiling_monthly')
					break;
				case 'annually':
					cur_frm.set_value('formatter', "annually");
					switch_show_hide_period_sections('billing_yearly')
					break;			
				default:
					break;
			}
		},
		error: (r) => {
			frappe.show_alert('Something went wrong!', 5)
		}
	})
}

function switch_show_hide_period_sections(period_section){
	cur_frm.set_df_property("billing_daily", "hidden", 1)
	cur_frm.set_df_property("biiling_monthly", "hidden", 1)
	cur_frm.set_df_property("billing_yearly", "hidden", 1)
	cur_frm.set_df_property(period_section, "hidden", 0)
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