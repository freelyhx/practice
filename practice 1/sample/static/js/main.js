function get_data_grid(){
     $.get('/datagrid','',function(data, status){
         if(status){
             var res = JSON.parse(data);
             var dg = res.result;
             var table = $('#table');
             
             $('.table-body').remove();
             for(var i in dg){
                table.append('<tr class="table-body"><td>' + i + '</td><td>'+ dg[i][0] +'</td><td>' + dg[i][1].toString() + '</td></tr>');
             }
         }
     });
}

$(document).ready(function(){
    get_data_grid();   
})

$(function () {
    $('#sign-in').click(function () {
        var session = localStorage['session'];
        if(typeof(session) == undefined){
            session='';
        };

        $.get('/count?user_id=' + session, '', function (data, status) {
            if (status) {
                console.log(JSON.parse(data));
                var res = JSON.parse(data);
                if(res.result){
                    localStorage['session'] = res.result;
                }
                get_data_grid();
            }
        })
    });
})