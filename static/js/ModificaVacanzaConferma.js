function confermaModificaVacanza(form){

	if(confirm("Sei sicuro di modificare la tua vacanza?")){
		form.submit();
		return true;
	}
	else{
		return false;
	}
}
