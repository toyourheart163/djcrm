// gbacc_ajax_login_js.js
// # ————————43PerfectCRM实现AJAX全局账号登陆————————
     $(function () {    // 页面加载完自动调用
            gbacc_ajax_login();
        });
     function gbacc_ajax_login() {
            $('#submit').click(function () {
                var $msg = $('#error_msg');//用来验证码错误 提示
                var sppwd=$('#sppwd');//密码
                $msg.parent().addClass('hide');//初始为隐藏提示标签  验证码
                sppwd.parent().addClass('hide');  //初始为隐藏提示标签 密码
                $.ajax({
                    url: '/gbacc/gbacc_ajax_login/',   //绑定验证的页面
                    type: 'POST',
                    data: $('#fm').serialize(),//表单所有内容
                    dataType: 'JSON',
                    success: function (arg) {
                        console.log(arg);
                        if(arg.status){
                            location.href = arg.next_url;//跳 转到 页面
                        }else{
                            //判断是否有这个错误信息
                            if(arg.usererror!=null){
                                sppwd.parent().removeClass('hide');
                                sppwd.text(arg.usererror);   // 密码
                            }
                            if(arg.chederror!=null){
                                $msg.parent().removeClass('hide');//移除隐藏提示标签
                                $msg.text(arg.chederror);
                            }
                            var img = $('#check_code_img')[0];//图片验证码变量
                            img.src = img.src + '?';//重载图片验证码
                            $('#check_code').val('');//密码和验证码框清空
                        }
                    }
                })
            })
        }
     //刷新验证码
     function loginchangeCheckCode(ths){
            ths.src = ths.src +  '?';
     }
// # ————————43PerfectCRM实现AJAX全局账号登陆————————

// gbacc_ajax_login_js.js