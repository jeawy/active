/*
 * Demo3:label样式
 */
 

$(document).ready(function() {
    $('.btn-set-primary').click(function() {
        var btn = $(this);
        var picid = btn.attr('picid');
        var productid = btn.attr('productid');
        var formData = new FormData(document.querySelector("#csrftocken_form"));
        formData.append('picid', picid);
        formData.append('productid', productid);
        $.ajax('/product/products/' + productid + '/', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data['status'] == 'OK') {
                    $().message(data['msg']);
                } else {
                    $().errormessage(data['msg']);
                }
            },
            error: function() {
                $().errormessage('server side error');
            }
        });
    });
    $('.btn-delete-primary').click(function() {
        var btn = $(this);
        var picid = btn.attr('picid');
        var productid = btn.attr('productid');
        var formData = new FormData(document.querySelector("#csrftocken_form"));
        formData.append('picid', picid);
        formData.append('productid', productid);
        formData.append('method', 'delete');
        $.ajax('/product/products/' + productid + '/', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data['status'] == 'OK') {
                    $().message(data['msg']);
                    // 3
                    setTimeout(function() {
                        location.reload();
                    }, 3000);
                } else {
                    $().errormessage(data['msg']);
                }
            },
            error: function() {
                $().errormessage('server side error');
            }
        });
    });
});