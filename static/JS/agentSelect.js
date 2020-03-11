$(function () {
    $("#Mymodal").click(function(){
        $("#new").modal("show")
    });

    var $main = $(".main");
    $main.css("width","1300px");
});

$(function(){
    let vm = new Vue({
        el:'#myDiv',
        delimiters:['{[', ']}'],
        data:{
            name:"",
            datas:[],
            maxShow:8,
            page:1,
            dataSize:Number,
            PageDatas:[]
        },
        methods:{
            submitData(event){
                event.preventDefault();
                $.ajax({
                    type:'GET',
                    url:'/search_1',
                    data:"search=target&name="+vm.name,
                    dataType:'json',
                    success:function(data){
                        vm.datas = data;
                        vm.dataSize = data.length;
                        if(vm.dataSize > vm.maxShow){
                            let start = (vm.page-1)*vm.maxShow;
                            let end = start + vm.maxShow;
                            vm.PageDatas = vm.datas.slice(start,end);
                        }else{
                            vm.PageDatas = vm.datas;
                        }

                    },
                    error:function(){
                        alert('发生异常！');
                    }
            });
            },

            ChangePage(flag){
                if(flag){
                    if((this.page)*this.maxShow < this.dataSize){
                        this.page++;
                        let start = (this.page-1)*this.maxShow;
                        let end = start + this.maxShow;
                        if(end >= this.dataSize){
                            this.PageDatas = this.datas.slice(start)
                        }else{
                            this.PageDatas = this.datas.slice(start,end);
                        }
                    }
                }else{
                    if(this.page>1){
                        this.page--;
                        let start = (this.page-1)*this.maxShow;
                        let end = start + this.maxShow;
                        this.PageDatas = this.datas.slice(start,end);
                    }
                }
            },

                    delItem(item,index){
                if(window.confirm("您确定要删除吗？")){
                    let workerID = item['worker_id'];
                    $.ajax({
                        type:'GET',
                        url:'/agentdelete',
                        data:"workerID="+workerID,
                        dataType:'json',
                        success:function(data){
                            if(data['status'] === "200"){
                                vm.datas.splice((vm.page-1)*vm.maxShow+index,1);
                                vm.PageDatas.splice(index,1);
                                alert(data['msg']);
                            }else{
                                alert(data['msg']);
                            }
                        },
                        error:function(){
                            alert('发生异常！');
                        }
                    });
            }
            },

        },
        mounted:function () {
          $.ajax({
                type:'GET',
                url:'/search_1',
                data:"search=all",
                dataType:'json',
                success:function(data){
                    vm.datas = data;
                    vm.dataSize = data.length;
                    if(vm.dataSize > vm.maxShow){
                        let start = (vm.page-1)*vm.maxShow;
                        let end = start + vm.maxShow;
                        vm.PageDatas = vm.datas.slice(start,end);
                    }else{
                        vm.PageDatas = vm.datas;
                    }
                },
                error:function () {
                    alert("error");
                }
            });
        }
    })
});