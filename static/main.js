$(document).ready(function () {

    $('#how-it-works').popover();

    var $form = $('#icon-generate-form');
    var $form_name = $form.find('#iconName');
    var $form_size = $form.find('#iconSize');
    var $form_color = $form.find('#iconColor');
    var $preview = $('.preview i');
    var $preview_warning = $('.preview .preview-size-warning');
    var $download_helper = $('#download-helper');
    var $generate_btn = $('#generate-btn');

    // *** send request to backend
    $form.submit(function (e) {
        e.preventDefault();

        $generate_btn.html('<i class="fa fa-spinner fa-spin"></i> Generating awesome..');
        $generate_btn.attr('disabled', 'disabled');

        $.getJSON('/generate?name=' + getName() + '&size=' + getSize() + '&color=' + getColor().replace('#', 'HASH'))
            .done(function (data) {
                if ('success' in data && data['success'] === true) {
                    [$form_name, $form_size, $form_color].forEach(function ($element) {
                        var $group = $element.parent().parent();
                        if (!$group.hasClass('has-success')) {
                            $group.addClass('has-success has-feedback');
                            $element.parent().append('<span class="fa fa-check form-control-feedback"></span>');
                        }
                    });

                    var url = window.location.origin + '/' + data['image_url'];

                    $download_helper.attr('href', url);
                    $download_helper.attr('download', url.split('/images/')[1]);
                    $download_helper.removeClass('hidden');
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var response = jqxhr['responseJSON'];

                if ('exception' in response) {
                    alert(response['exception']);
                }
                else if ('errors' in response) {
                    for (var error in response['errors']) {
                        var $element;
                        switch (error) {
                            case 'name': $element = $form_name; break;
                            case 'size': $element = $form_size; break;
                            case 'color': $element = $form_color; break;
                            default: break;
                        }
                        if ($element !== undefined) {
                            var $group = $element.parent().parent();
                            if ($group.hasClass('has-error')) {
                                $element.parent().find('.help-block').html(response['errors'][error]);
                            }
                            else {
                                $group.addClass('has-error has-feedback');
                                $element.parent().append('<span class="fa fa-times form-control-feedback"></span>');
                                $element.parent().append('<span class="help-block">' + response['errors'][error] + '</span>');
                            }
                        }
                    }
                }
            }).always(function() {
                $generate_btn.html('<i class="fa fa-cogs"></i> Generate Icon');
                $generate_btn.removeAttr('disabled');
            });
    });

    // *** preview
    $form.find('input').change(function () {
        var $this = $(this);
        var $group = $this.parent().parent();

        if ($group.hasClass('has-error')) {
            $group.removeClass('has-error');
            $this.parent().find('.help-block').remove();
        }

        if ($group.hasClass('has-success')) {
            $group.removeClass('has-success');
        }

        if ($group.hasClass('has-feedback')) {
            $group.removeClass('has-feedback');
            $this.parent().find('.form-control-feedback').remove();
        }

        var size = getSize();

        if (size > 100) {
            size = 100;
            $preview_warning.removeClass('hidden');
        } else {
            $preview_warning.addClass('hidden');
        }

        $preview.attr('style', 'font-size:' + size + 'px; color:' + getColor());
        $preview.attr('class', 'fa fa-' + getName());

        $download_helper.addClass('hidden');
    });

    function getName() {
        return $form_name.val().replace(' ', '').replace(/^fa-+/, '');
    }

    function getSize() {
        return parseInt($form_size.val().replace(' ', '').replace('px', ''));
    }

    function getColor() {
        return $form_color.val().replace(' ', '');
    }
});
