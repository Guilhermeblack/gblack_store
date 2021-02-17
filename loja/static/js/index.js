
//Adicionar produtos ao carrinho

function add_prod(produ){


    var produto = produ;
    var csrf = $('#csrfmiddlewaretoken').val();
    console.log('foi aqui', csrf);
    $.ajax({
        headers: { "X-CSRFToken": csrf },
        type: 'POST',
        url: "prod",
        data: {'add_carrinho' :produto},

        success: function (response) {

        },
        error: function (response) {
        }
    });

};