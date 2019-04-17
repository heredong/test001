$(function () {
    $('button').click(function () {

        var name = $("#uname").val();
        var pwd = $("#pwd").val();
        var confirm_pwd = $("#confirm_pwd").val();
        var email = $("#email").val();
        var file = $("#icon")[0].files[0];
        console.log(name);
        console.log(pwd);
        console.log(email);
        console.log(name.length);
        console.log(this.length);
        console.log('开始判断');
        if (name.length <=3){
            alert('用户名过短');
            return
        }
        if (pwd!=confirm_pwd){
            alert('密码和确认密码不一致');
            return
        }
        var enc_pwd = md5(pwd);
        var enc_confirm_pwd = md5(confirm_pwd);

        if (file.size == 0){
            alert("请选择头像");
            return
        }
        var formdata = new FormData();
        formdata.append("username", name);
        formdata.append("pwd", enc_pwd);
        formdata.append("confirm_pwd", enc_confirm_pwd);
        formdata.append("email", email);
        formdata.append("icon", file);

        $.ajax({
            url:"/api/shopping/v1/register",
            data:formdata,
            processData:false,
            cache:false,
            contentType:false,
            method:'post',
            success:function (res) {
                console.log(res);
                if (res.code == 0){
                    window.open(res.data,target='_self')
                    console.log('跳转')
                }else {
                    alert(res.msg);
                    console.log('错误')
                }

            },
            fail:function (res) {
                console.log('跳转失败')

            }
        })

    })

})
