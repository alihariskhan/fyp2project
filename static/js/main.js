
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
                success: function (response) {
                    // Handle success with SweetAlert2
                    Swal.fire({
                        icon: 'success',
                        title: 'Application Submitted Successfully!',
                        text: response,
                    });

                    // Reset the form
                    $('#jobApplicationForm')[0].reset();
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
