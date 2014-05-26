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

        if (name) {
            $.getJSON('/generate?name=' + name + '&size=' + size + '&color=' + color, function () {
            })
                .done(function (data) {
                    var image = window.location.origin + '/' + data['icon_url'];
                    var $helper = $('#download-helper');
                    $helper.attr('href', image);
                    $helper.attr('download', image.split('/images/')[1]);
                    $helper.removeClass('hidden');
                })
                .fail(function (jqxhr, textStatus, error) {
                    try{
                        alert(jqxhr['responseJSON']['custom_error']);
                    } catch (e) {
                        alert('Epic fail! Sorry, I didn\'t see this coming. Please try again.')
                    }
                })
                .always(function (data) {
                });
        } else {
            alert('Please enter the name of the font awesome icon you wish to download, I can\'t read your mind! Though my creators are working on that, I heard.')
        }
    });

    function getName(form) {
        var name = form.find('#iconName').val();
        name = name.replace(' ', '').replace('fa-', '');
        return name
    }

    function getSize(form) {
        var size = form.find('#iconSize').val();
        size = size.replace(' ', '').replace('px', '');
        if (parseInt(size) > 1024) {
            alert('Hey mate, please stay under 1024px. Working on a ラーメン (ramen) budget here ;)');
        }
        return size
    }

    function getColor(form) {
        var color = form.find('#iconColor').val();
        color = color.replace(' ', '').replace('#', '');
        if (color.length = !6) {
            alert('Hey mate, please use full 6 digit hex values. Maybe soon I\'ll get a smarter form validation.');
        }
        return color
    }

    // *** Preview
    $('#icon-generate-form').find('input').change(function () {
        var $preview = $('.preview i');
        var form = $('#icon-generate-form');
        var name = getName(form);
        var size = getSize(form);
        var color = getColor(form);

        if (parseInt(size) > 100) {
            size = 100;
            if ($('#iconName').val().length > 2) {
                $('.preview .preview-size-warning').removeClass('hidden');
            }
        } else {
            $('.preview .preview-size-warning').addClass('hidden');
        }

        $preview.attr('style', 'font-size:' + size + 'px ; color: #' + color);
        $preview.attr('class', 'fa fa-' + name);

        $('#download-helper').addClass('hidden');
    });
});
