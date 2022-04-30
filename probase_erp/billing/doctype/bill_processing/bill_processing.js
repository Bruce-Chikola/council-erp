// Copyright (c) 2022, Probase Limited and contributors
// For license information, please see license.txt
frappe.ui.form.on('Bill Processing', {
	setup:(frm)=>{
		// frm.disable_save()
		frm.toggle_display("occupied_by", frm.doc.item_group=="Pads");
		$('[data-fieldname="status"],[data-fieldname="failed"],[data-fieldname="successful"],[data-fieldname="total"]').hide()
		createLoaderHtmlCss();
	},
	refresh: function(frm) {
		addCss()
		// frm.disable_save()
		$('[data-fieldname="failed"],[data-fieldname="successful"],[data-fieldname="total"]').hide()
		// add button to process bills
		console.log(frm.doc)
		if(frm.doc.docstatus == 1){
			frm.add_custom_button('Process Bills',()=>{
				var data = {
					doc_name:frm.doc.name,
					billing_profile:frm.doc.billing_profile,
					bill_type:frm.doc.bill_type,
					start_date: frm.doc.start_date,
					completion_date:frm.doc.completion_date,
					frequency:frm.doc.frequency,
					billing_period:frm.doc.billing_period
				};
				(data.start_date < data.completion_date || data.start_date == data.completion_date)? 
				startBillProcessing(data) : frappe.show_alert('Completion date can not be lower or same as Start date!', 5);
	
			}).addClass("primary bill-process-btn").css({'color':'white',background:'#07A0D0',wdith:'200px !important',
				display:'flex', alignItems:'center', justifyContent:'center'
			})
		}
		// style input fields
		// $('input[autocomplete="off"]:not(#navbar-search),select[autocomplete="off"],.control-value.like-disabled-input').css({
		// 	background:'transparent',border:'1px #BFC7CA solid',height:'34px'
		// })	
		//route to bills
		frm.add_custom_button('View Bills History',()=>frappe.set_route('bills'))
	},
	// to automatically set the next date depending on the billing profile content
	'billing_profile':(frm)=>getBillingDependantFields(frm),
	// to automatically set the next date depending on the frequency, when start date is changed
	'start_date':(frm)=>calculateFutureDate(frm.doc.start_date, frm.doc.frequency)
});

// function to get Billing frequency
function getBillingDependantFields(frm){
	frappe.call({
		method: 'probase_erp.billing.overrides.bill_processor.get_profile_dependand_fields',
		args: {billing_profile_name:frm.doc.billing_profile},
		freeze: true,
		callback: (r) => {
			cur_frm.set_value('frequency', r.message[0]);
			cur_frm.set_value('bill_type', r.message[1]);
			calculateFutureDate(frm.doc.start_date, frm.doc.frequency)
		},
		error: (r) => frappe.show_alert("Couldn't Fetch DEpendant Fields", 5)
	})
}

// to create the next date for the bill
function calculateFutureDate(currentDate,frequency){		
	if(currentDate){
		var current = new Date(currentDate);
		switch (frequency.toLowerCase()) {
			case 'daily':
				current.setDate(current.getDate() + 1)
				break;
			case 'weekly':
				current.setDate(current.getDate() + 7)
				break;
			case 'monthly':
				current.setMonth(current.getMonth()+1)
				break;	
			case 'annually':
				current.setFullYear(current.getFullYear()+1)
				break;
			default:
				break;		
		}
		cur_frm.set_value('completion_date', current);
	}
}


// to send billing info to the back end
function startBillProcessing(data){
	$('.bill-process-btn').html('Processing Bills <div class="btn-loader"></div>').prop('disabled',true)
	frappe.call({
		method: 'probase_erp.billing.overrides.bill_processor.process_bills',
		args: data,
		freeze: true,
		callback: (response) => {
			setTimeout(() => {$('.bill-process-btn').html('Process Bills').prop('disabled',false)}, 1000);
			frappe.show_alert(response.message, 5);
		},
		error: (r) => {
			$('.bill-process-btn').html('Process Bills').prop('disabled',false)
			frappe.show_alert('An error occurred!', 5)
		}
	})
	
}

function addCss(){
	$('.ellipsis.title-text').css({
		fontSize:13,padding:'5px 5px',
		minWIdth:'200px',
		background:'linear-gradient(80deg,#1388C3,#29A3E0)',
		color:'white',
		borderRadius:5
	})
}


// function to create loader html.
function createLoaderHtmlCss(){
	$('head').append(`
		<style>
			.btn-loader{
				width:15px;
				height:15px;
				margin-left:5px;
				border-radius:50%;
				border-top:2px white dotted;
				border-right:2px white solid;
				border-bottom:2px white solid;
				border-left:2px transparent dotted;
				animation: load-bill-processor 1s linear infinite;
				transition: .2s;
			}
			@keyframes load-bill-processor{
				from{transform:rotate(0deg)}
				to{transform:rotate(360deg)}
			}
		</style>
	
	`);
}