$(document).ready(function() {
    var optimum_total_cost = $('#optimum_total_cost').text();
    var optimum_project_duration = $('#optimum_project_duration').text();

    $('#results_table table tbody tr').each(function() {
        project_duration = $(this).children(':nth-child(1)').text();
        total_cost = $(this).children(':nth-child(5)').text();

        if (total_cost == optimum_total_cost && project_duration == optimum_project_duration) {
            $(this).attr('class', 'optimum-solution');
        }
    });
});
