$(document).ready(function() {
    // Toggle form mode
    $('#takeBtn').click(function() {
        $('#actionField').val('take');
        $('#takeBtn').addClass('active');
        $('#returnBtn').removeClass('active');
    });

    $('#returnBtn').click(function() {
        $('#actionField').val('return');
        $('#returnBtn').addClass('active');
        $('#takeBtn').removeClass('active');
    });

    // Load components when category changes
    $('#categorySelect').change(function() {
        const category = $(this).val();
        $('#componentSelect').html('<option>Loading...</option>');

        $.get(`/components/${category}`, function(data) {
            let options = '<option value="" disabled selected>Select component</option>';
            data.forEach(comp => {
                options += `<option value="${comp.id}">${comp.name}</option>`;
            });
            $('#componentSelect').html(options);
        }).fail(function() {
            $('#componentSelect').html('<option value="" disabled>Error loading components</option>');
        });
    });
});