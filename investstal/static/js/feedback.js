//Feedback Form
let feedback = {
    submit: function($form) {
        let formURL = $form.attr('action');
        let data = new FormData();
        let form_array = $form.serializeArray();
        for (let i = 0; i < form_array.length; i++) {
            data.append(form_array[i].name, form_array[i].value);
        }
        $.ajax({
            url: formURL,
            data:  data,
            processData: false,
            contentType: false,
            method: 'POST',
            success: function(data) {
                let modal = $form.parents('.modal');

                $form.replaceWith(data).show();

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