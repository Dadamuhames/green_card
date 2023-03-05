$('.dropzone').each((i, e) => {
    Dropzone.options.myAwesomeDropzone = false;
    Dropzone.autoDiscover = false;
    var myDropzone = new Dropzone(e, {
        url: $(e).attr("data-url"),
        parallelUploads: 1,
        maxFiles: $('.dropzone').attr('data-max'),
        acceptedFiles: 'image/*',
        params: {
            "csrfmiddlewaretoken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "key": $(e).attr('data-key'),
            'id': $('input[name="id"]').val(),
            'url': window.location.href
        },
        previewsContainer: `#${$(e).find('.dz-preview-container').attr('id')}`,
        success: (file, response) => {
            var removeButton = Dropzone.createElement(`<a class="dz-remove" data-dz-remove>Удалить</a>`);
            removeButton.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                myDropzone.removeFile(file);

                data = {}
                data["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val()
                data['key'] = $('input[name="dropzone-key"]').val()
                data['file'] = response

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