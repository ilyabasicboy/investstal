$(function(){
    let groups = $('.field-group select');
    groups.each(function() {
        if(!$(this).val()) {
            $(this).parents('.form-row').find('.field-value select').prop('disabled', true);
        }
    });

    $(document).on('change', '.field-group select', function(){
        let parameter_field = $(this).parents('.form-row').find('.field-value select')
        let value = $(this).val();
        if (value) {
            let data = {
                'parameter_group': $(this).val(),
            };
            $.get('/custom_catalog/parameters_list/', data, function(data){
                parameter_field.html(data);
                parameter_field.prop('disabled', false);
            });
        }
        else {
            parameter_field.val('');
            parameter_field.prop('disabled', true);
        }
    });
});
