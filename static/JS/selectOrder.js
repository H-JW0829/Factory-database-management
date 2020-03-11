/**
 * Created by 黄佳威 on 2020/2/27.
 */
$(function () {
               let ordervm = new Vue({
                el:"#myDiv2",
                delimiters:['{[', ']}'],
                data:{
                    canDel:true,
                    orderTime:"",
                    customerInfo:"",
                    datas:[],
                    showButton:false,
                    labels:["订单号","公司名称","下单日期","交付日期","交付状态"],
                    maxShow:8,
                    page:1,
                    dataSize:Number,
                    PageDatas:[],
                    canEdit:false
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
                        data:"time="+this.orderTime+"&customer="+this.customerInfo+"&select=order",
                        dataType:'json',
                        success:function(data){
                            ordervm.datas = data;
                            ordervm.dataSize = data.length;
                            // console.log("--------------dataSize------------");
                            // console.log(workervm.dataSize);
                            // console.log("--------------dataSize------------");
                            if(ordervm.dataSize > ordervm.maxShow){
                                let start = (ordervm.page-1)*ordervm.maxShow;
                                let end = start + ordervm.maxShow;
                                ordervm.PageDatas = ordervm.datas.slice(start,end);
                            }else{
                                ordervm.PageDatas = ordervm.datas;
                            }
                            // console.log("--------------pagedata------------");
                            // console.log(workervm.PageDatas);
                            // console.log("--------------pagedata------------");
                            console.log(data);
                            console.log(data);
                            var buttons = document.getElementsByClassName("btn btn-primary btn-lg");
                            if(buttons.length > 0){
                                 buttons[0].click();
                            }
                        },
                        error:function () {
                            alert("error");
                        }
                    });

                    },

                    delItem(item,index){
                        if(window.confirm("您确定要删除吗？")){
                            let orderNum = item['order_num'];
                            $.ajax({
                                type:'POST',
                                url:'/delete',
                                data:"type=order&orderNum="+orderNum,
                                dataType:'json',
                                success:function(data){
                                    if(data['status'] === "200"){
                                        ordervm.datas.splice(index,1);
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

                }
                })
            });