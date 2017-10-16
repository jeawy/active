

 



$('.activetype').click(function(){
        var activetype = $(this).val();
        if (activetype == 1){
            $('.activecost').show('slow');
        }else{
            $('.activecost').hide('slow');
        }
    });
//  发表+存稿按钮    >>> 点击事件
$('.product-btn').click(function() { 
    var title = $('#title').val();
    var desc = $('#desc').val();

    var detail = tinymce.get("detail").getContent();
     
    
    var pricefrom  = $('#pricefrom').val();
    var priceto = $('#priceto').val();

    var location = $('#location').val();
 

    var datefrom = $('#datefrom').val(); 

    var activetype = $('input[name=activetype]:checked').val();
 
    data = {
        'method': 'create', 
        'title': title,
        'description': detail , 
        'pricefrom': pricefrom,
        'priceto': priceto,

        'datefrom': datefrom, 
        'activetype':activetype, 
        'location': location, 
        'status': $(this).attr('status'),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    var product = $('#productid');
    if (product.length > 0){
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }
    
    
    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function(result) {
            if(result['status'] == 'ok'){
                $().message(result['msg']);
                setTimeout(function() {
                    window.location.href="/product/products/"+result['id']+"/";
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
});

//  属性设置    >>> 添加属性
$('#add-pro').click(function() {
    $(".alert-text").remove();
    var pro = $('#pro').val();
    var val = $('#val').val();
    var proTr = '<tr class="parameter_tr">' +
        '<td class="key">' + pro + '</td>' +
        '<td class="value">' + val + '</td>' +
        '<td><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
        '</tr>';

    if (pro.length == 0 || val.length == 0) {
        var html = '<div class="alert-text">内容不能为空!</div>';
        $('#pro-table').before(html);
    } else {
        $('#pro-table').append(proTr);
        $('#pro,#val').val("");
    };
});

//  属性设置    >>> 删除行
$('#pro-table').on('click', '.fa-trash-o', function() {
    $(this).parent().parent().remove();
});

//  内容简介    >>> 输入字数监听     
$(".ta-wrap input").on('keyup input', function(event) {
    console.log(event.type)
    var val = $(this).val();
    var len = val.length;
    var count = $(this).siblings('span');

    if (len == 0) { count.text("0/50"); return; }
    if (len > 50) {
        len = 50;
        $(this).val(val.substring(0, 50));
    }
    count.text(len + "/50");
});


$('.activetype').click(function(){
    var activetype = $(this).val();
    if (activetype == 1){
        $('.activecost').show('slow');
    }else{
        $('.activecost').hide('slow');
    }
});
///以下是修改product时用到的js

$( ".datefrom" ).datetimepicker( {language:'zh-CN',}); 
$("#pricefrom, #priceto").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
         // Allow: Ctrl+A, Command+A
        (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) || 
         // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
             // let it happen, don't do anything
             return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});