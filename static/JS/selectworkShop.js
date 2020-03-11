/**
 * Created by 黄佳威 on 2020/2/27.
 */
$(function () {
               let workshopvm = new Vue({
                el:"#myDiv3",
                delimiters:['{[', ']}'],
                data:{
                    workShopNum:"",
                    canDel:false,
                    datas:[],
                    showButton:false,
                    labels:["车间号","车间主任ID","车间电话"],
                    PageDatas:[]
                },
                methods:{
                    submitData(event){
                        event.preventDefault();
                        this.showButton = true;
                        $.ajax({
                        type:'POST',
                        url:'/select',
                        data:"workshopID="+this.workShopNum+"&select=workshop",
                        dataType:'json',
                        success:function(data){
                            workshopvm.datas = data;
                            workshopvm.dataSize = data.length;
                            // console.log("--------------dataSize------------");
                            // console.log(workervm.dataSize);
                            // console.log("--------------dataSize------------");
                            if(workshopvm.dataSize > workshopvm.maxShow){
                                let start = (workshopvm.page-1)*workshopvm.maxShow;
                                let end = start + workshopvm.maxShow;
                                workshopvm.PageDatas = workshopvm.datas.slice(start,end);
                            }else{
                                workshopvm.PageDatas = workshopvm.datas;
                            }
                            // console.log("--------------pagedata------------");
                            // console.log(workervm.PageDatas);
                            // console.log("--------------pagedata------------");
                            var buttons = document.getElementsByClassName("btn btn-primary btn-lg");
                            console.log(buttons);
                            if(buttons.length > 0){
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
                }
                })
            });