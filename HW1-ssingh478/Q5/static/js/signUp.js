$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
                if (JSON.parse(response).status=="OK"){
				$('#successAlert').text('Congratulations on registering for CSE6242, '+JSON.parse(response).user+'! Redirecting you to the course homepage...').show();
				$('#errorAlert').hide();
				console.log(response);
				$('form').trigger('reset');
                setTimeout(function() {
  window.location.href = "http://poloclub.gatech.edu/cse6242/";
}, 3000);}
                else{
                	var errmess= [' 1. Should be at least 8 characters in length',' 2.Should have at least 1 uppercase character',' 3.Should have at least 1 number'];
                var i;
                var texted="";
for (i = 0; i <= JSON.parse(response).pass.length-1; i++) {
    texted += errmess[JSON.parse(response).pass[i]-1];
}

                $('#successAlert').text(JSON.parse(response).user+', the password is invalid because it,'+texted+'. Please try again!').show();
                $('#errorAlert').hide();
				console.log(response);
                $("input[type='password']").val('');
				//$('form').trigger('reset');

                }

			},
			error: function(error){
				$('#errorAlert').text("Please fill both fields").show();
				$('#successAlert').hide();
				//console.log(error);
			}

		});
//$('#form').trigger("reset");

  	});

});
