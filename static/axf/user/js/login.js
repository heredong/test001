$(function () {
    $('button').click(function () {
        var name = $("#uname").val();
        var pwd = $("#pwd").val();
        console.log(name)
        console.log(pwd)
        console.log(name.length)
        console.log(pwd.length)
        if (name.length==0 || pwd.length==0){
            alert('用户名或密码不能为空');
            return;
        }

        var enc_pwd = md5(pwd);
        console.log(enc_pwd)
        $.ajax({
            url:'/api/shopping/v1/login',
            data:{
                uname: name,
                pwd:enc_pwd,

            },
            method:'post',
            success:function (res) {
                console.log(res.code)
                console.log(res.msg)
                if (res.code == 0){
                    window.open(res.data,target='_self')

                }else {
                    alert(res.msg);
                }

            },
            fail:function () {

            },
            complete:function () {
                
            }

        })
    })

})