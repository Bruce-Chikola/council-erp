// Copyright (c) 2022, probase and contributors
// For license information, please see license.txt

frappe.ui.form.on('Booth Fee Charges', {
	refresh: function(frm) {
		addCss()
	}
});

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