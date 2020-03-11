//在页面加载时候，就使td节点具有click点击能力
$(function(){
    //给所有td添加点击事件
    let liNods = $(".li_edit>span");
    $(".li_edit>span").change(updateInDB);
    liNods.dblclick(liClick);//点击调用tdClick方法
    function liClick() {
        //点击时将文本框内容保存、插入输入框、将文字写入输入框
        // 将td的文本内容保存
        let li = $(this);
        let ulChildren = li.parent("li").children();
        let liText = li.text();//未修改的值
        // 将li的内容清空
        li.empty();
        // 新建一个输入框
        let input = $("<input>");
        // 将保存的文本内容赋值给输入框
        input.val(liText);
        input.css("width","200px");
        // 将输入框添加到td中
        li.append(input);
        // 双击获取基础数据
        input.dblclick(function() {
        });
        input.blur(function() {
            // 将输入框的文本保存
            let input = $(this);
            let inputText = input.val();
            // 将td的内容，即输入框去掉,然后给td赋值
            let li = input.parent("span");
            li.html(inputText);//修改后的值
        });
        // 将jquery对象转化为DOM对象
        let inputDom = input.get(0);
        inputDom.select();
        // 将td的点击事件移除
        li.unbind("click");
    }
    function updateInDB() {
        setTimeout(function () {
            let spans = $(".li_edit>span");
            let name = spans[0].innerText;
            let idCardNo = spans[1].innerText;
            let age = spans[2].innerText;
            let contartInfo = spans[3].innerText;
            let address = spans[4].innerText;
            let sex = spans[5].innerText;
            //console.log(name,idCardNo,age,contartInfo,address,sex);
            $.ajax({
                type:'GET',
                url:'/updateuser',
                data:"name="+name+"&idCardNo="+idCardNo+"&age="+age+"&contartInfo="+contartInfo+"&address="+address+"&sex="+sex,
                //data:"msg=success",
                dataType:'json',
                success:function(data){
                    if(data['status']==='200'){
                        alert(data['msg']);
                    }else{
                        alert(data['msg']);
                    }
                },
                error:function () {
                    alert("操作错误，请待会重试或咨询管理员！");
                }
            });
        },1);
    }
});
