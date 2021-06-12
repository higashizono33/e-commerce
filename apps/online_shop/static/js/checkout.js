$(document).ready(
    $('.order_qty').on('change', function(e){
        e.preventDefault();
        var qty = $(this)
        $.ajax({
            type: 'get',
            url: 'cart/update_item',
            data: qty.parent().serialize(),
            success: function(response){
                var i = qty.attr('id')
                $('#id-'+i+'-cost').text('$'+response.cost)
                $('#sub-total').text('$'+response.sub_total)
                $('#shipping-cost').text('$'+response.shipping_cost)
                $('#total').text('$'+response.total)
            }
        })
    }),
    $('body').on('click', '.trash-bin', function(e){
        e.preventDefault();
        var itemId = $(this).attr('itemId')
        $.ajax({
            type: 'get',
            url: 'cart/delete_item/'+itemId,
        }).done(function(response){
            $('#sub-total').text('$'+response.sub_total)
            $('#shipping-cost').text('$'+response.shipping_cost)
            $('#total').text('$'+response.total)
            $('tbody').html(response.table)
            $('.item_count').text(response.item_count)
        })
    }),
    $('#same-address').on('click', function(){
        var first_name = $('#shipping').find('#id_first_name').val()
        var last_name = $('#shipping').find('#id_last_name').val()
        var address = $('#shipping').find('#id_address').val()
        var address2 = $('#shipping').find('#id_address2').val()
        var city = $('#shipping').find('#id_city').val()
        var state = $('#shipping').find('#id_state').val()
        var zipcode = $('#shipping').find('#id_zipcode').val()
        
        $('#billing').find('#id_first_name').val(first_name)
        $('#billing').find('#id_last_name').val(last_name)
        $('#billing').find('#id_address').val(address)
        $('#billing').find('#id_address2').val(address2)
        $('#billing').find('#id_city').val(city)
        $('#billing').find('#id_state').val(state)
        $('#billing').find('#id_zipcode').val(zipcode)
    })
)