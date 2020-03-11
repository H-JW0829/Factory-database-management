/**
 * Created by 黄佳威 on 2020/2/27.
 */
$(function () {
       let productvm = new Vue({
        el:"#myDiv5",
        delimiters:['{[', ']}'],
        data:{
            canDel:true,
            productId:"",
            datas:[],
            showButton:false,
            labels:["产品编号","产品名称","出售价格","利润","产量"],
            maxShow:8,
            page:1,
            dataSize:Number,
            PageDatas:[]
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
                data:"product_id="+this.productId+"&select=product",
                dataType:'json',
                success:function(data){
                    productvm.datas = data;
                    productvm.dataSize = data.length;
                    // console.log("--------------dataSize------------");
                    // console.log(workervm.dataSize);
                    // console.log("--------------dataSize------------");
                    if(productvm.dataSize > productvm.maxShow){
                        let start = (productvm.page-1)*productvm.maxShow;
                        let end = start + productvm.maxShow;
                        productvm.PageDatas = productvm.datas.slice(start,end);
                    }else{
                        productvm.PageDatas = productvm.datas;
                    }
                    // console.log("--------------pagedata------------");
                    // console.log(workervm.PageDatas);
                    // console.log("--------------pagedata------------");
                    console.log(data);
                    console.log(data);
                    console.log(data);
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

            delItem(item,index){
                if(window.confirm("您确定要删除吗？")){
                    let product = item['product_id'];
                    console.log("-----------------------");
                    console.log(product);
                    console.log("-----------------------");
                    $.ajax({
                        type:'POST',
                        url:'/delete',
                        data:"type=product&productId="+product,
                        dataType:'json',
                        success:function(data){
                            if(data['status'] === "200"){
                                workervm.datas.splice(index,1);
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
