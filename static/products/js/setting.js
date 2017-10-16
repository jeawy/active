　
function submitclick( data ){  
    var product = $('#productid');
    if (product.length > 0){
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }
    data['csrfmiddlewaretoken'] = getCookie('csrftoken');
    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function(result) {
            if (result['status'] == 'ok'){
                $().message(result['msg']);
                setTimeout(function() {
                    location.reload();
                }, 3000);
            }else{
                $().errormessage(result['msg']);
            }
        },
        error: function() {
            // 500
            alert('server is down!')
        }
    })
}

$('.btn-book-set-homepage').click(function() { 
    var set_homepage =  $(this).attr('sethomepage');
    data = {  'set_homepage': set_homepage };
    submitclick( data );
 });
 $('.btn-book-set-grid').click(function() { 
    var set_grid =  $(this).attr('setgrid');
    data = {  'set_grid': set_grid };
    submitclick( data );
 });