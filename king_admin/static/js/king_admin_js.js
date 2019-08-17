function SelectALLObjs(ele) {
    if ($(ele).prop('checked')){
        $('input[row-select]').prop('checked',true)

    }else{
         $('input[row-select]').prop('checked',false)
    }
}

function ActionCheck(ele){
    var selected_action = $("select[name='action']").val();
    var selected_objs = $("input[row-select]").filter(":checked");
    console.log($("select[name='action']").val())
    if (!selected_action){
        alert("no action selected!")
        return false
    }
    if (selected_objs.length == 0 ){
        alert("no object selected!")
        return false
    }else {
        //生成一个标签,放到form里

        var selected_ids = [];
        $.each(selected_objs,function () {
            console.log($(this) );
            selected_ids.push($(this).val())
        })
        console.log(selected_ids)
        var input_ele = "<input type='hidden' name='selected_ids' value=" + JSON.stringify(selected_ids) + ">"

        $(ele).append(input_ele);
    }
}