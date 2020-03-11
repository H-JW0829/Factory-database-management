$(function () {
   let producevm = new Vue({
    el:"#myDiv7",
    delimiters:['{[', ']}'],
    data:{
        canDel:false,
        orderNum:"",
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
            data:"orderNum="+this.orderNum+"&select=orderProduct",
            dataType:'json',
            success:function(data){
                producevm.datas = data;
                producevm.dataSize = data.length;
                if(producevm.dataSize > producevm.maxShow){
                    let start = (producevm.page-1)*producevm.maxShow;
                    let end = start + producevm.maxShow;
                    producevm.PageDatas = producevm.datas.slice(start,end);
                }else{
                    producevm.PageDatas = producevm.datas;
                }
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
