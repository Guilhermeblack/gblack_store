        $(document).on('click','#pix_btn', function(){

            var dados  = $(this).val();
            dados = dados.split('_');

            $.ajax({
                headers: { "X-CSRFToken": csrf },
                type: 'POST',
                url: url_pag,
                dataType: "json",
                data: {
                    'valor_pagamento' :dados[0],
                    'tipo_pagamento':dados[1],
                    'usuario':dados[2]
                },
                success: function (response) {
                },
                error: function (response) {
                }
            });

        });

        $(document).on('blur','#pdt_nome', function(){
            var prod = $(this).text().split(':')[1];

            var proid = $(this).siblings('#pdt_id').val();
            console.log('dalipdt >', proid);
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                type: 'POST',
                url: "{% url 'prod' %}",
                dataType: "json",
                data: {
                    'pdt_nome' :prod,
                    'proid':proid
                },
                success: function (response) {

                },
                error: function (response) {
                }
            });

        });

        $(document).on('blur','#pdt_est', function(){
            var prod = $(this).text().split(':')[1];
            var proid = $(this).siblings('#pdt_id').val();
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                type: 'POST',
                url: "{% url 'prod' %}",
                dataType: "json",
                data: {
                    'pdt_est' :prod,
                    'proid':proid
                },
                success: function (response) {
                },
                error: function (response) {
                }
            });

        });

        $(document).on('blur','#pdt_des', function(){
            var prod = $(this).text().split(':')[1];
            console.log('dalipdt >', prod);
            var proid = $(this).siblings('#pdt_id').val();
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                type: 'POST',
                url: "{% url 'prod' %}",
                dataType: "json",
                data: {
                'proid':proid,
                'pdt_des' :prod
                },
                success: function (response) {
                },
                error: function (response) {
                }
            });

        });

        $(document).on('blur','#pdt_pre', function(){
            var prod = $(this).text().split(':')[1];
            console.log('dalipdt >', prod);
            var proid = $(this).siblings('#pdt_id').val();
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                type: 'POST',
                url: "{% url 'prod' %}",
                dataType: "json",
                data: {
                    'proid':proid,
                    'pdt_pre' :prod
                },
                success: function (response) {
                },
                error: function (response) {
                }
            });


        });

        $(document).on('blur','#pdt_tipo', function(){
            var prod = $(this).val();
            console.log('éoprod', prod);
            var proid = $(this).parent().siblings('#pdt_id').val();
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                type: 'POST',
                url: "{% url 'prod' %}",
                dataType: "json",
                data: {
                    'pdt_tipo' :prod,
                    'proid':proid
                },
                success: function (response) {
                },
                error: function (response) {
                }
            });

        });

        $(document).on('click','#btn_del',function(){
            var prod = $(this).val();
            var proid = $('#pdt_id').siblings('#pdt_id').val();
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                type: 'POST',
                url: "{% url 'prod' %}",
                dataType: "json",
                data: {
                    'btn_del' :prod,
                    'proid':proid
                },
                success: function (response) {
                },
                error: function (response) {
                }
            });

        });
        $(document).on('click','data-toggle',function(e) {
            if( $(e.target).is('a') ) {
                $(this).collapse('hide');
            }
        });