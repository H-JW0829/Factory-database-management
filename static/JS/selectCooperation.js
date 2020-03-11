/**
 * Created by 黄佳威 on 2020/2/27.
 */
      $(function () {
   let companyvm = new Vue({
    el:"#myDiv4",
    delimiters:['{[', ']}'],
    data:{
        canDel:false,
        companyName:"",
        datas:[],
        showButton:false,
        labels:["公司名称","联系方式","联系人姓名","地址"],
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
            data:"companyName="+this.companyName+"&select=cooperation",
            dataType:'json',
            success:function(data){
                companyvm.datas = data;
                companyvm.dataSize = data.length;
                if(companyvm.dataSize > companyvm.maxShow){
                    let start = (companyvm.page-1)*companyvm.maxShow;
                    let end = start + companyvm.maxShow;
                    companyvm.PageDatas = companyvm.datas.slice(start,end);
                }else{
                    companyvm.PageDatas = companyvm.datas;
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