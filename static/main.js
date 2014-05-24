$(document).ready(function () {

    // *** activate BS alert functionality
    $('.alert').alert();


    // *** send request to backend
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
                    console.log(data['icon_url']);
                    var image = window.location.origin + '/' + data['icon_url'];
                    var $helper = $('#download-helper');
                    $helper.attr('href', image);
                    $helper.attr('download', image.split('/images/')[1]);
                })
                .fail(function (jqxhr, textStatus, error) {
                    alert('Fail, please check your input values.');
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


    // *** Preview
    $('#icon-generate-form').find('input').change(function(form) {
        var $preview = $('.preview i');
        $preview.attr('style', 'font-size:' + $('#iconSize').val() + 'px ; color: #' + $('#iconColor').val() );
        $preview.attr('class', 'fa fa-' + $('#iconName').val());
    });

});
