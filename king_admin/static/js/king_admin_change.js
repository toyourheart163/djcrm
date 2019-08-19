// king_admin_change.js
// # ————————27PerfectCRM实现King_admin编辑复选框————————
        function BeforeFormSubmit(form_ele) {

            console.log(form_ele);
            //$('form input[disabled]').prop("disabled", false);//修改为可提交
            $("form").find("[disabled]").removeAttr("disabled");//修改为    可提交

            $('select[m2m_right="yes"] option').prop('selected', true);

            return true;
        }


        function MoveEleTo(from_ele, target_ele_id) {
            //move options from from_ele to target ele
            var field_name = $(from_ele).parent().attr("field_name");//获option名
            if (target_ele_id.endsWith('_from')) {//判断是否
                var new_target_id = "id_" + field_name + "_to";
            } else {
                var new_target_id = "id_" + field_name + "_from";
            }
            //创建一个新标签
            var opt_ele = "<option value='" + $(from_ele).val() + "'  ondblclick=MoveEleTo(this,'" + new_target_id + "')  >" + $(from_ele).text() + "</option>";
            $("#" + target_ele_id).append(opt_ele);//添加到另一边选框
            $(from_ele).remove();//移除选中的

        }

// # ————————27PerfectCRM实现King_admin编辑复选框————————

// king_admin_change.js