function getCookie(name) {
        // Function to get any cookie available in the session.
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    var page_title = $(document).attr("title");
    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


$(document).ready(function(){
	/*Variables*/
	let form = $('form');
	let email_input = form.find('input[name=email]');
	let load_ = form.find('.lds-ellipsis');
	
	const form_url = form.attr('action');
	const validate_url = '/validate/';
	const duration = 1500;

	/*show newsletter*/
	setTimeout(function(e){
		form.find('input[name=email]').parents('.row').slideDown()
	},duration);

	/*handles form*/
	form.on('submit',function(e){
		e.preventDefault();
		
		let request_data = {
			'content':email_input.val(),
			'csrf_token':csrftoken
		}


		load_.show();


		if(!(email_input.val().length > 1)){
			email_input.removeClass('success');
			email_input.removeClass('error');
			return false
		}
		
			$.ajax({
					url : form_url,
					data: request_data,
					type: 'POST',
					dataType:'json',
					cache: false,
					success : function(response){
						if(response.data == true){
							email_input[0].value = '';
							load_.hide();
						}
						else{
							load_.hide();
							console.log('already taken');
						}
					},
					error : function(error){
						console.log(error);

					}

			});
		return false;		

	});


	/*handle email field only*/
	email_input.on('keyup',function(e){
		e.preventDefault();
		let value_ = $(this).val();
	
		if(!(value_.length > 2)){
			email_input.removeClass('success');
			email_input.removeClass('error');
			return false
		}

		let email_data = {
			'content': value_,
			'csrf_token':csrftoken
		}

			$.ajax({
					url : validate_url,
					data: email_data,
					type: 'POST',
					dataType:'json',
					cache: false,
					success : function(response){
						if(response.data == true){
							email_input.removeClass('success');
							email_input.addClass('error');
						}
						else{
							email_input.addClass('success');
							email_input.removeClass('error');
						}
					},
					error : function(error){
						console.log(error);
					}

			});
		return false;
		
	})
});