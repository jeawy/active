
$(document).ready(function(){
     $('.div-select').dropdown({
         input: '<input type="text" maxLength="20" placeholder="Search">',
         searchable: true,
         choice: function () {
             $('.search-form').submit();
         } ,
        searchNoData: '<li style="color:#ddd">No Results</li>', 
     });

      $( ".datefrom" ).datepicker({ 
            defaultDate: "+1w",
            changeMonth: true,
            changeYear: true,
            language:'zh-CN', 
            format:'yyyy-mm-dd', 
        }); 
         $( ".dateto" ).datepicker({ 
            defaultDate: "+1w",
            changeMonth: true,
            changeYear: true,
            language:'zh-CN', 
            format:'yyyy-mm-dd', 
        }); 
 
   
    $(".pricefrom, .priceto").keydown(function (e) {
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
    
});


/* */
var aList=$('.p-list-categary');
var oDate=new Date();//取今天的日期  
var oNow=oDate.getFullYear()+'/'+(oDate.getMonth()+1)+'/'+oDate.getDate(); 
oNow =Date.parse(oNow);
for(var i=0;i<aList.length;i++){
    var startTime = $(aList[i]).attr('datefrom');
    startTime = startTime.replace(/-/g,"/");//替换字符，变成标准格式         
    var d1 = Date.parse(startTime);       
    if(d1<oNow){  
      $(aList[i]).parents('.row').find('.p-list-name').append('<span class="abate">已结束</span>');  
      
    }  
}

 
