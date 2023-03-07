$("form.epilogue").on('submit', (e) => {
    e.preventDefault()
    let username = $(e.target).find('input[name="username"]')

    data = {}
    data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val()
    data['username'] = username.val()

    $.ajax({
        url: '/check_username',
        type: 'POST',
        data: data,
        success: (data) => {
           console.log(data)

           if(data == 'success') {
            $(e.target).submit()
           } else {

            for(let key in data) {
                $(e.target).find(`input[name="${key}"] + .error-p`).html(data[String(key)])
            }
           }
        }
    })
})