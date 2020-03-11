/**
 * Created by 黄佳威 on 2020/2/27.
 */
$(function () {
   let workervm = new Vue({
    el:"#myDiv1",
    delimiters:['{[', ']}'],
    data:{
        canDel:true,
        workerType:"",
        workerAge:"",
        carRoom:"",
        datas:[],
        PageDatas:[],
        showButton:false,
        labels:["员工","姓名","身份证号","年龄","性别","电话","地址","工资","工种","所属车间","操作"],
        maxShow:8,
        page:1,
        dataSize:Number,
        canEdit:true,
        showEdit:true
    },
    methods:{
        submitData(event){
            console.log(this.showButton);
            event.preventDefault();
            this.showButton = true;
            console.log(this.labels);
            $.ajax({
            type:'POST',
            url:'/select',
            data:"staff_type="+this.workerType+"&staff_age="+this.workerAge+"&staff_car_room="+this.carRoom+"&select=worker",
            dataType:'json',
            success:function(data){
                workervm.datas = data;
                workervm.dataSize = data.length;
                if(workervm.dataSize > workervm.maxShow){
                    let start = (workervm.page-1)*workervm.maxShow;
                    let end = start + workervm.maxShow;
                    workervm.PageDatas = workervm.datas.slice(start,end);
                }else{
                    workervm.PageDatas = workervm.datas;
                }
                var buttons = document.getElementsByClassName("btn btn-primary btn-lg");
                console.log(buttons);
                if(buttons.length > 0) {
                    buttons[0].click();
                }
            },
            error:function () {
                alert("error");
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
                    type:'POST',
                    url:'/delete',
                    data:"type=worker&workerID="+workerID,
                    dataType:'json',
                    success:function(data){
                        if(data['status'] === "200"){
                            workervm.datas.splice((workervm.page-1)*workervm.maxShow+index,1);
                            workervm.PageDatas.splice(index,1);
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

        editItem(item,itemIndex){

        }
    }
    })
});