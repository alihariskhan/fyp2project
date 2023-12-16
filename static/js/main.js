$(document).ready(function () {
    // Use event delegation for dynamically added elements
    $(document).on("submit", "#jobApplicationForm", function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Serialize form data
        var formData = $(this).serialize();

        // Make AJAX request
        $.ajax({
            type: "POST",
            url: "/jobapply",
            data: formData,
            success: function (response, status, xhr) {
                // Check the status code returned by the server
                if (xhr.status === 201) {
                    // Handle "Already Submitted!" response with SweetAlert2
                    Swal.fire({
                        icon: 'warning',
                        title: 'Already Submitted!',
                        text: response,
                    });
                } else if (xhr.status === 200) {
                    // Handle success for other cases
                    Swal.fire({
                        icon: 'success',
                        title: 'Application Submitted Successfully!',
                        text: response,
                    });

                    // Reset the form
                    $('#jobApplicationForm')[0].reset();
                }
                else if (xhr.status === 202) {
                    // Handle success for other cases
                    Swal.fire({
                        icon: 'warning',
                        title: 'Application Already Rejected!',
                        text: response,
                    });
                }
                else if (xhr.status === 203) {
                    // Handle success for other cases
                    Swal.fire({
                        icon: 'warning',
                        title: 'Already Rejected in Interview!',
                        text: response,
                    });
                }
            },
            error: function (error) {
                // Handle error with SweetAlert2
                Swal.fire({
                    icon: 'error',
                    title: 'Error Submitting Application',
                    text: error.responseText,
                });
            }
        });
    });
});
