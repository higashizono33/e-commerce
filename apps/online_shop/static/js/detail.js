$(document).ready(
    $('.buy-btn').on('click', function(e){
        e.preventDefault();
        var itemId = $(this).attr('item_id')
        $.ajax({
            type: 'post',
            headers: {"X-CSRFToken": '{{csrf_token}}'},
            url: '/show/'+itemId,
            data: $(this).parent().serialize(),
            success: function(response){
                $('.item_count').text(response.item_count)
            }
        })
        $("#popUp").fadeIn(); 
        setTimeout(function() {
            $("#popUp").fadeOut();
        }, 1500);
    }),
    $('.product_image').on('click', function() {
        var clicked_image =  $(this).attr('src')
        var main_image =  $('.main_image').attr('src')
        $(this).attr('src', main_image)
        $('.main_image').attr('src', clicked_image)
    })
)