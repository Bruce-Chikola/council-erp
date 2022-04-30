// Copyright (c) 2021, Probase Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property', {
    setup: function (frm) {
        cur_frm.set_df_property("rentals_details_section", "hidden", 1)
    },

    refresh: function (frm) {
        // $('input[autocomplete="off"]:not(#navbar-search),select[autocomplete="off"],.control-value.like-disabled-input').css({
		// 	background:'transparent',border:'1px #BFC7CA solid'
		// })	
        console.log(frm.doc)
        cur_frm.set_df_property("rentals_details_section", "hidden", 1)
        // add button to process bills
		frm.add_custom_button('Create Billing Profile',()=>{
			frappe.set_route('billing-profile/new-billing-profile-1')

		})
    },
    'is_rentals_exempted':function(frm){
        $('[data-fieldname="is_rentals_exempted"]').find('.disp-area').find('input').hasClass('disabled-selected') ?
        cur_frm.set_df_property("rentals_details_section", "hidden", 1) :cur_frm.set_df_property("rentals_details_section", "hidden", 0);
    }
});





