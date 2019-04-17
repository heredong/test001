$(function () {
    $(".all_select").click(function () {
        $.ajax({
            url: '/api/shopping/v1/cart-status',
            success:function (res) {
                if(res.code==0){
                    //    更新全选按钮状态
                    var text = res.data.is_select_all?"√":"";
                    $(".all_select>span>span").text(text);
                    //    更新总价
                    $("#sum_money").text(res.data.sum_money);
                    //    更新商品选中状态
                    $(".confirm").each(function () {
                        $(this).find('span').find('span').text(text);
                    })
                }


            }
        })
    });
    $(".confirm").click(function () {
        var $current_btn=$(this);
        var cid = $current_btn.parents('li').attr("cart_id");

        $.ajax({
            url:'/api/shopping/v1/cart/status',
            data:{
                cid:cid
            },
            method:'put',
            success:function (res) {
                if(res.code==0){
                    //修改当前数据选中状态
                    if (res.data.is_select_all){
                        $('.all_select>span>span').html('√');
                    }
                    }else {
                        $('.all_select>span>span').html('');
                    }

                $("#sum_money").html(res.data.money);
                if(res.data.current_item_status){
                    $current_btn.find('span').find('span').html('√')
                }else{
                    $current_btn.find('span').find('span').html('')
                }
            }
        })
    });
    $(".addCart").click(function () {
        var $btn = $(this);
        var cid = $btn.parents('li').attr('cart_id');
        $.ajax({
            url:'/api/shopping/v1/cart/options',
            data:{
                cid:cid,
                option:'add',
            },
            method: 'put',
            success:function (res) {
                if(res.code==0){
                    $btn.prev().text(res.data.current_num);
                    $("#sum_money").text(res.data.sum_money)
                }else {
                    alert(res.msg)
                }
            }
        })
    })
    $(".subCart").click(function () {
        var $btn = $(this);
        var cid = $btn.parents('li').attr('cart_id');
        $.ajax({
            url:'/api/shopping/v1/cart/options',
            data:{
                cid:cid,
                option:'sub',
            },
            method: 'put',
            success:function (res) {
                if(res.code==0){
                    if (res.data.current_num!=0){
                    $btn.next().text(res.data.current_num);
                    $("#sum_money").text(res.data.sum_money)
                    }else {
                        $btn.parents('li').remove();
                    }
                }else {
                    alert(res.msg)
                }
                var text = res.data.is_select_all?'√':"";
                $(".all_select>span>span").text(text);
            }
        })
    })
})