$("form.epilogue").on('submit', (e) => {
    e.preventDefault()

    data = $(e.target).serialize()
    let url = $(e.target).attr('action')

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        success: (data) => {
           console.log(data)

           if(data != 'success' && 'username' in data) {
               $(e.target).find(`input[name="username"] + .error-p`).html(data.username)
           } else {
            window.location.reload()
           }
        }
    })
})