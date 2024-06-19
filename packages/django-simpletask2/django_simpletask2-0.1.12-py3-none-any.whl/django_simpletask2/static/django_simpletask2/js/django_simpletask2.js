; (function ($) {
    $(document).ready(function () {
        $(".django_simpletask2_channel_admin_button").click(function (event) {
            event.stopPropagation();
            var confirm_message = $(this).attr("confirm-message");
            var action_request_failed_message = $(this).attr("action-request-failed-message");
            var request_url = $(this).attr("href");
            var result = confirm(confirm_message);
            if (result) {
                $.ajax({
                    url: request_url,
                    method: "GET",
                    success: function (data) {
                        if (data.code != 0) {
                            alert(data.message);
                        } else {
                            window.location.reload();
                        }
                    },
                    error: function (data) {
                        console.log(data);
                        alert(action_request_failed_message);
                    }
                });
            }
            return false;
        });
    });
})(jQuery);
