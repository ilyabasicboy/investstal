//Feedback Form
let feedback = {
	submit: function($form) {
		let formURL = $form.attr('action');
		let data = new FormData();
		let form_array = $form.serializeArray();
		for (let i = 0; i < form_array.length; i++) {
			data.append(form_array[i].name, form_array[i].value);
		}

		//Add files form
		const fileInput = $form.find('input[type=file]');
		if (fileInput.length > 0){
            for (let file of fileInput[0].files) {
                if (file) {
                    data.append('file', file);
                }
            }
        }

		$.ajax({
			url: formURL,
			data:  data,
			processData: false,
			contentType: false,
			method: 'POST',
			success: function(data) {
				let modal = $form.parents('.modal');

				$form.replaceWith(data);

				//Hide title in modal
				if (data.match(/thank-you/) && modal.length > 0) {
					modal.find('.modal__header').hide();
				}
			},
		});
		return false;
	}
};

//Ajax Send
$(document).on('submit', '.feedback-form', function(e) {
	e.preventDefault();
	feedback.submit($(this));
});

//Custom Switch
$('body').on('click', '.switch', function(){
	let form_selector = '#'+$(this).parents('form').attr('id');
	$(form_selector+' .switch').removeClass('active');
	$(this).addClass('active');
	if($(this).hasClass('on')){
		$(form_selector+' [name$="flag"]').val('on');
	}
	if($(this).hasClass('fake1')){
		$(form_selector+' [name$="flag"]').val('fake1');
	}
	if($(this).hasClass('fake2')){
		$(form_selector+' [name$="flag"]').val('fake2');
	}
	if($(this).hasClass('fake3')){
		$(form_selector+' [name$="flag"]').val('fake3');
	}
});

//File Length
$(document).on('change', '.input-file', function (e) {
	let $this = $(this);
	//Old DataTransfer
	let dt = $this.data('dt');

	//Create new DataTransfer
	if (!dt) {
		dt = new DataTransfer();
		$this.data('dt', dt);
	}

	let filelength = $this[0].files.length;
	let items = $this[0].files;
	let fileTotalSize = 5242880;

	//Check type
	const isImageOnly = $this.is('[data-accept-img]');
	const isImageAndFile = $this.is('[data-accept-imgfile]');
	const validImageTypes = ['image/jpeg', 'image/png'];
	const validFileTypes = [
		'image/jpeg',
		'image/png',
		'application/pdf',
		'application/vnd.oasis.opendocument.text',
		'application/vnd.ms-excel'
	];

	//Error
	let $error = $this.closest('.upload').find('.upload__error');
	if ($this.data('errorTimer')) {
		clearTimeout($this.data('errorTimer'));
	}
	let hasError = false;

	if (filelength > 0) {
		for (let i = 0; i < filelength; i++) {
			let isValidType = false;

			//Type
			if (isImageOnly) {
				isValidType = validImageTypes.includes(items[i].type);
			} else if (isImageAndFile) {
				isValidType = validFileTypes.includes(items[i].type);
			} else {
				isValidType = true;
			}

			if (items[i].size > fileTotalSize) {
				//Show error
				$error.text('Допустимый размер 5 MB').show();
				hasError = true;

				//Hide error
				$this.data('errorTimer', setTimeout(function() {
					$error.text('').hide();
				}, 2000));

				continue;
			} else if (!isValidType) {
				//Show error
				$error.text('Неверный формат').show();
				hasError = true;

				//Hide error
				$this.data('errorTimer', setTimeout(function() {
					$error.text('').hide();
				}, 2000));

				continue;
			} else {
				//Add file name to list
				let fileBlock = $('<li/>', { class: 'upload__list-item' }),
					fileName = $('<span/>', { class: 'upload__list-name', text: items[i].name }),
					fileDeleteBtn = $('<span/>', { class: 'upload__list-delete' });

				fileBlock.append(fileName).append(fileDeleteBtn);
				$this.closest('.upload').find('.upload__list').append(fileBlock);

				//Add file to DataTransfer
				dt.items.add(items[i]);
			}
		}

		//Update files
		$this[0].files = dt.files;
	}

	//Clear error
	if (!hasError) {
		$error.text('').hide();
		if ($this.data('errorTimer')) {
			clearTimeout($this.data('errorTimer'));
		}
	}

	//Delete file
	$this.parent().parent().parent().find('.upload__list-delete').off('click').on('click', function () {
		let name = $(this).prev('span.upload__list-name').text();
		let input = $(this).parents('.upload').find('.input-file');
		let dt = input.data('dt');

		$(this).parent().remove();

		for (let i = 0; i < dt.items.length; i++) {
			if (name === dt.items[i].getAsFile().name) {
				dt.items.remove(i);
				break;
			}
		}

		input[0].files = dt.files;
	});
});

//Reload form
function ajaxReset($form) {
	let formURL = $form.data('reset-url');
	let formKey = $form.data('key');
	$.ajax({
		url: formURL,
		data:  { 'form_key' : formKey },
		method: 'GET',
		success: function(data) {
			let modal = $form.parents('.modal');

			$form.replaceWith(data).show();

			//Show title in modal
			if (modal.length > 0) {
				modal.find('.modal__header').show();
			}
		}
	});
	return false;
};

//Export Function
export default ajaxReset;