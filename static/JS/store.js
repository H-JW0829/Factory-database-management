$(function () {
  let storeVm = new Vue({
    el:"#myTabContent",
    delimiters:['{[', ']}'],
    data:{
        datas:[],
        maxShow:8,
        page:1,
        dataSize:Number,
        PageDatas:[],
        lessdatas:[],
        lessPageDatas:[],
        lessPage:1,
        lessDataSize:Number
    },
    methods:{
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
                let productID = item['product_id'];
                let warehouseID = item['warehouse_id'];
                var that = this;
                $.ajax({
                    type:'GET',
                    url:'/delete_store',
                    data:"productID="+productID+"&warehouseID="+warehouseID,
                    dataType:'json',
                    success:function(data){
                        if(data['status'] === "200"){
                            that.datas.splice((that.page-1)*that.maxShow+index,1);
                            that.PageDatas.splice(index,1);
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
      let that = this;
      $.ajax({
            type:'GET',
            url:'/getstore',
            dataType:'json',
            success:function(data){
                if(data[0]["status"] === "200"){
                    that.datas = data.slice(1);
                    that.dataSize = that.datas.length;
                    if(that.dataSize > that.maxShow){
                        let start = (that.page-1)*that.maxShow;
                        let end = start + that.maxShow;
                        that.PageDatas = that.datas.slice(start,end);
                    }else{
                        that.PageDatas = that.datas;
                    }

                    for(let i = 0;i < that.dataSize;i++){
                        if(Number(that.datas[i]["quantity"]) <= 3){
                            that.lessdatas.push(that.datas[i]);
                        }
                    }
                    that.lessDataSize = that.lessdatas.length;
                    if(that.lessDataSize > that.maxShow){
                        let start = (that.lessPage-1)*that.maxShow;
                        let end = start + that.maxShow;
                        that.lessPageDatas = that.lessdatas.slice(start,end);
                    }else{
                        that.lessPageDatas = that.lessdatas
                    }
                }else{
                    alert("获取数据失败！");
                    console.log(data);
                }
            },
            error:function () {
                alert("error");
            }
        });
    }
});
});