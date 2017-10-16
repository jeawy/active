
$(document).ready(function(){
     var map = new AMap.Map('map_container', {
        resizeEnable: true,
        zoom:11,
        center: [116.452463,39.914812]
    });
   
    var marker = new AMap.Marker({
        position: [116.452463,39.914812],
        title: '世贸天阶',
        map: map
    });
   
//步行
$('.fa-street-view').click(function(e){
    e.preventDefault();
    map.clearMap();
     AMap.plugin(["AMap.Walking"], function() {
            var drivingOption = { 
                map:map,
                panel: "panel"
            };
            var walking = new AMap.Walking(drivingOption); //构造驾车导航类
              //根据起终点坐标规划驾车路线
            walking.search(
                [116.379028, 39.865042], [116.427281, 39.903719],
                function(status,result){
                    $('#panel').empty();
                });
        });
});
       
//公交车
$('.fa-bus').click(function(e){
    e.preventDefault();
    map.clearMap();
     AMap.plugin(["AMap.Transfer"], function() {
            var drivingOption = {
                city:'北京',
                 panel: "panel",
                policy:AMap.TransferPolicy.LEAST_TIME,
                map:map,
                
               
            };
            var transfer = new AMap.Transfer(drivingOption); //构造驾车导航类
              //根据起终点坐标规划驾车路线
            transfer.search(
                [{keyword:'北京站'},{keyword:'北京大学'}],
                function(status,result){
                    $('#panel').empty();
                });
        });
});
//骑车
$('.fa-bicycle').click(function(e){
    e.preventDefault();
    map.clearMap();
     AMap.plugin(["AMap.Riding"], function() {
            var drivingOption = {
                policy:AMap.DrivingPolicy.LEAST_TIME,
                map:map,
                panel: "panel"
            };
            var riding = new AMap.Riding(drivingOption); //构造驾车导航类
              //根据起终点坐标规划驾车路线
            riding.search(
                [{keyword:'北京站'},{keyword:'北京大学'}],
                function(status,result){ 
                    $('#panel').empty();
                });
        });
});
//驾车
$('.fa-car').click(function(e){
    e.preventDefault();
    map.clearMap();
    $('#panel').empty();
     AMap.plugin(["AMap.Driving"], function() {
            var drivingOption = { 
                map:map,
                panel: "panel"
            };
            var driving = new AMap.Driving(drivingOption); //构造驾车导航类
              //根据起终点坐标规划驾车路线
            driving.search(
                [{keyword:'北京站'},{keyword:'北京大学'}],
                function(status,result){
                    //
                });
        });
});
$('.btn-book').click(function(e){
    e.preventDefault();
    var auth = $('#auth').val();
    if (auth == '0'){
        $().errormessage('请先登录...');
        setTimeout(function() {
                window.location.href = '/users/login/?next='+window.location.pathname;
        }, 2000); 
    }else{
        $('#book').modal('toggle');  
    }
})
// 提交预定情况
$('.btn-submit').click(function(){
    var formData = new FormData(document.querySelector("#signup-Form"));
    var productid = $('#productid').val();
    var auth = $('#auth').val();
    if (auth == '0'){
        $().errormessage('请先登录...');
        setTimeout(function() {
                window.location.href = '/users/login/?next='+window.location.pathname;
        }, 2000);
            
    }
    $.ajax('/product/products/'+productid+'/addatt', {
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
        if (data['status'] == 'OK') {
                $().message(data['msg']);
                setTimeout(function() {
                  location.reload();
              }, 3000);
            }
            else {
                $('body').append('<label class="err_label" >' + data['msg'] + '</label>'); //
            }
        },
        error: function () {
            alert('Server down...');
        }
    });
})
 
});

