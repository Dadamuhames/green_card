$(document).ready(() => {
    $('.sidebar__link').each((i, e) => {
        console.log(e.href)
        if (e.href == window.location.href || e.href == location.protocol + '//' + location.host + location.pathname) {
            $(e).addClass('active')
        }
    })
})



$('div.my-dropzone').each((i, e) => {
    console.log($(e).attr('data-accept'))
    Dropzone.options.myAwesomeDropzone = false;
    Dropzone.autoDiscover = false;
    var myDropzone = new Dropzone(e, {
        url: '/save_images',
        parallelUploads: 1,
        acceptedFiles: String($(e).attr('data-accept')),
        //acceptedFiles: 'image/*',
        params: {
            "csrfmiddlewaretoken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "key": $(e).attr('data-key'),
            'id': $('input[name="id"]').val(),
            'url': window.location.href
        },
        previewsContainer: `#${$(e).find('.dz-preview-container').attr('id')}`,
        success: (file, response) => {
            var removeButton = Dropzone.createElement(`<a class="dz-remove" data-dz-remove>Удалить</a>`);
            removeButton.addEventListener("click", function (ev) {
                ev.preventDefault();
                ev.stopPropagation();
                myDropzone.removeFile(file);

                data = {}
                data["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val()
                data['key'] = $(e).attr('data-key')
                data['file'] = response
                console.log($(e).attr('data-delete'))

                $.ajax({
                    url: $(e).attr('data-delete'),
                    type: 'POST',
                    data: data,
                    success: () => {
                        console.log('success')
                    },
                    error: () => {
                        console.log('error')
                    }

                })

            });
            file.previewElement.appendChild(removeButton);
        }
    });


})



function submit_form(id) {
    console.log(id)
    let form = $(`#${id}`)
    let url = form.attr("action")
    let data = $(`#${id} :input`).serialize()

    $.ajax({
        url: url,
        data: data,
        type: 'POST',
        success: () => {
            $(form).parent().remove()
        }
    })

}