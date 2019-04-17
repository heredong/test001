$(function () {
    var types_menu_is_down = true;
    var sort_menu_is_down = true;

    $("#all_type").click(function () {
        sub_type_toggle();
    })

    $("#sub_types").click(function () {
        sub_type_toggle();
    })

    $("#all_sort").click(function () {
        sort_toggle();
    })
    $("#sort").click(function () {
        sort_toggle();
    })

    function sort_toggle() {
        $("#sort").toggle();
        if (sort_menu_is_down){
            $("#all_sort").find('span').find('span').removeClass('glyphicon glyphicon-menu-down');
            sort_menu_is_down=false;
        }else {
            $("#all_sort").find('span').find('span').removeClass('glyphicon glyphicon-menu-up');
            sort_menu_is_down = true;
        }

    }

    function sub_type_toggle() {
        $("#sub_types").toggle();
        if (types_menu_is_down){
            $("#all_type").find('span').find('span').removeClass('glyphicon glyphicon-menu-down');
            types_menu_is_down=false;
        }else {
            $("#all_type").find('span').find('span').removeClass('glyphicon glyphicon-menu-up');
            types_menu_is_down=true;
        }

    }

    $(".addShopping").click(function () {
        var goods_id = $(this).attr('goods_id');
        var $current_btn = $(this);
        console.log(goods_id);
        $.ajax({
            url:'/api/shopping/v1/cart_item',
            data:{
                goods:goods_id,
                num:1,
            },
            method:'post',
            success:function (res) {
                // console.log(res)
                if (res.code==1){
                    window.open(res.data,target='_self')
                }else if(res.code==0){
                    $current_btn.prev().html(res.data.num)
                }else {
                    alert(res.msg)
                }
            }
            }

        )
    })

    $(".subShopping").click(function () {
        var goods_id = $(this).attr('goods_id');
        var $current_btn = $(this);
        // console.log(goods_id);
        if ($current_btn.next().text()=='0'){
            return
        }
        $.ajax({
            url:'/api/shopping/v1/cart_item',
            data:{
                goods:goods_id,
                num:1,
            },
            method:'put',
            success:function (res) {
                console.log(res)
                if (res.code==1){
                    window.open(res.data,target='_self')
                }else if(res.code==0){
                    $current_btn.next().html(res.data)
                }else {
                    alert(res.msg)
                }
            }
            }

        )
    })

})