$(document).ready(
    $('.status').on('change', function(e){
        e.preventDefault();
        $.ajax({
            type: 'get',
            url: 'orders/update_status',
            data: $(this).parent().serialize(),
        })
    }),
    $('#nav_order').css('border-bottom', '1px Solid white')
)
    