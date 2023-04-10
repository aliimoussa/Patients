/* API endpoints */
//
var endpoint_get_patients = 'https://patients-977g.onrender.com/patients';
var endpoint_get_patient_medications = `https://patients-977g.onrender.com/api/patients/patient_id/medications`;
var endpoint_upload_csv = 'https://patients-977g.onrender.com/api/upload_csv';


/* paging variable */
var current_page = 1;

/* prevent XSS attacks by encoding special characters */
function clean(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/* paging logic, update page number and make action */
function update_page(number, callback = false) {

    current_page = number;
    callback ? callback() : '';

}

/* reset filters and paging and get data */
function reset_filters(number, callback = false) {

    $('#search').val('');
    current_page = 1;
    callback ? callback() : '';

}

function build_patients_data() {
    var table_body = 'patients_data';
    var all_patients = ``;

    /* search and filters data */
    var search = $('#search').val();
    var column_name = $('#sort-column').val();
    var age = $('#from_age').val();

    $('#load_more_patients_data, #loading_patients_data').remove();

    if (current_page == 1) {
        document.getElementById(table_body).innerHTML = `<tr id="loading_patients_data"><td colspan="12">Loading ...</td></tr>`;
    } else {
        document.getElementById(table_body).innerHTML += `<tr id="loading_patients_data"><td colspan="12">Loading ...</td></tr>`;
    }



    var json_data = JSON.stringify({
            "search": search,
            "column_name": column_name,
            "age":age,
            "page": current_page
        });

    $.ajax({
    url: endpoint_get_patients,
    type: "POST",
    contentType: "application/json",
    data: json_data,
    success: function (response) {
            var response_error = response.error;
            var response_error_message = response.message;
            var response_data = response.data;
            var total_patients = response.total_items;
            $('#total_patients').text(total_patients);
            if (response_error) {
                alert(response_error_message);
                document.getElementById(table_body).innerHTML = `<tr><td colspan="12">No data</td></tr>`;
            } else {
                $('#loading_patients_data').remove();
                if (current_page === 1 && response_data.length === 0) {
                    document.getElementById(table_body).innerHTML = `<tr><td colspan="12">No data</td></tr>`;
                } else {
                    $('#loading_patients_data').remove();
                    if (response_data.length === 0) {
                    } else {
                        $(response_data).each(function () {
                            all_patients += `<tr>`;
                            all_patients += `<td>${clean(this.first_name)} ${clean(this.last_name)}</td>`;
                            all_patients += `<td>${clean(this.phone_number)}</td>`;
                            all_patients += `<td>${clean(this.date_of_birth)}</td>`;
                            all_patients += `<td>${clean(this.address)}</td>`;
                            all_patients += `<td>${String(clean(this.insurance_plan)) !== 'null' ? clean(this.insurance_plan) : 'N/A'}</td>`;
                            all_patients += `<td class="text-center">
                    <button data-id="${clean(this.id)}" class="btn-sm btn btn-main meds w-100 btn-fix">Show</button>
                    </td>`;
                            all_patients += `</tr>`;
                        });

                        all_patients += `<tr id="load_more_patients_data" >
                                    <td colspan="12" class="text-center">
                                        <button class="btn-sm btn btn-outline-secondary btn-fix my-2" style="width:160px">Load More</button>
                                    </td>
                                </tr>`;

                        if (current_page == 1) {
                            document.getElementById(table_body).innerHTML = all_patients;
                        } else {
                            $('#loading_patients_data').remove();
                            if (response_data.length == 0) {
                            } else {
                                document.getElementById(table_body).innerHTML += all_patients;
                            }
                        }
                    }
                }
            }
        }
});


}


function build_patient_meds_data(patient_id) {
    var patient_medications = 'patient_medications';
    var all_meds = ``;
    document.getElementById(patient_medications).innerHTML = `<tr><td colspan="12">Loading ...</td></tr>`;
    $.get(endpoint_get_patient_medications.replace('patient_id', patient_id), function (response) {

        var response_error = response.error;
        var response_error_message = response.message;
        var response_data = response.data;

        if (response_error) {
            alert(response_error_message);
        } else {
            $('#patient_meds_modal').modal('show');
            $(response_data).each(function () {
                all_meds += `<tr>`;
                all_meds += `<td>${this.name}</td>`;
                all_meds += `<td>${this.dosage}</td>`;
                all_meds += `<td>${this.frequency}</td>`;
                all_meds += `<td>${this.start_date}</td>`;
                all_meds += `<td>${this.end_date}</td>`;
                all_meds += `</tr>`;
            });
            document.getElementById(patient_medications).innerHTML = all_meds;
        }
    });
}

function build_years_data(from = 18) {
    var years = '.years';
    var all_options = `<option value="">All</option>`;
    for (let index = from; index <= 100; index++) {
        all_options += `<option value="${index}">${index}</option>`;
    }
    $(years).html(all_options);
}

/* delay user input before getting the value */
var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

/* initialize data */
$(function () {

    /* create ages lists started from 18 years old */
    build_years_data(18);

    update_page(1, build_patients_data);

});

/* user filter event on text search */
$(document).on('input', '#search, #sort-by, #from_age', function () {

    /* get and show patients data for example 700 ms */
    delay(function () {

        update_page(1, build_patients_data)

    }, 700);

});

/* get medications */
$(document).on('click', '.meds', function () {

    /* get patient medication */
    var patient_id = $(this).data('id');
    build_patient_meds_data(patient_id);

});

/* user filter event on change on of the select list */
$(document).on('change', '#sort-column, #from_year, #to_year', function(){

    /* get and show patients data */
    update_page(1, build_patients_data);

});

/* load more patients */
$(document).on('click', '#load_more_patients_data', function () {

    update_page((current_page + 1), build_patients_data);

});

/* get medications */
$(document).on('change', '.uploader', function () {

    var data = new FormData();
    jQuery.each($(this)[0].files, function (i, file) {
        data.append('file', file);
    });

    $.ajax({
        url: endpoint_upload_csv,
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        type: 'POST',
        success: function (response) {

            /* analyze response and check data (errors etc.) */

            if (response.error) {

                alert(response.message);

            } else {

                /* if all data are valid */
                alert('Success! Data was imported');

                /* refresh patients data */
                reset_filters(1, build_patients_data);

            }

        }
    });

});

