$(function () {
    $(".delete").click(function () {
        var $btn = $(this);
        var order_item_id = $btn.parents('li').attr('order_item_id')
        var order_id = $("h3").text().split(":")[1]
        $.ajax({
            url:"/api/shopping/v1/orderitem",
            method:"delete",
            data:{
                pk:order_item_id,
                order_id:order_id
            },
            success:function (res) {
                if(res.code==0){
                    $(".pay_msg").text('待付款金额：￥'+res.data.sum_money);
                    $btn.parents('li').remove()
                }
            }
        })
    })
})