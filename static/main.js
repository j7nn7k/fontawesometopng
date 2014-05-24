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

        console.log(name, size, color);

        if (name && size && color) {
            $.getJSON('/generate?name=' + name + '&size=' + size + '&color=' + color, function () {
            })
                .done(function (data) {
                    console.log(data['icon_url']);
                })
                .fail(function (jqxhr, textStatus, error) {
                    console.log('fail');
                    // console.log("Status " + textStatus);
                    // console.log("Error " + error);
                })
                .always(function (data) {
                });
        }
    });

    function getName(form) {
        return form.find('#iconName').val();
    }

    function getSize(form) {
        return form.find('#iconSize').val();
    }

    function getColor(form) {
        return form.find('#iconColor').val();
    }

});
