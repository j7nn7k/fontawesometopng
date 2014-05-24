$(document).ready(function () {
    // activate BS alert functionality
    $('.alert').alert();

    // send request to backend
    $('#icon-generate-form').submit(function (e) {
        e.preventDefault();
        var form = $(this);

        var name = getName(form);
        var size = getSize(form);
        var color = getColor(form);

        if (name && size && color) {
            $.getJSON('/generate?name=' + name + '&size=' + size + '&color=' + color, function () {
            })
                .done(function (data) {
                    console.log("success");
                })
                .fail(function (jqxhr, textStatus, error) {
                    console.log("Status " + textStatus);
                    console.log("Error " + error);
                })
                .always(function (data) {
                });
        }

    });

    function getName(form) {
        form.find('#iconName').val();
    }

    function getSize(form) {
        form.find('#iconName').val();
    }

    function getColor(form) {
        form.find('#iconName').val();
    }

});
