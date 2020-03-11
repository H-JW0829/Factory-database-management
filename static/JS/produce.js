$(function () {
       let productvm = new Vue({
        el:"#myDiv5",
        delimiters:['{[', ']}'],
        data:{
            canDel:true,
            workshopId:"",
            datas:[],
            showButton:false,
            labels:["车间号","产品号"],
            maxShow:8,
            page:1,
            dataSize:Number
        },
        methods:{
            submitData(event){
                console.log(this.showButton);
                event.preventDefault();
                this.showButton = true;
                console.log(this.labels);
                $.ajax({
                type:'POST',
                url:'/select/5',
                data:"product_id="+this.productId+"&select=product",
                dataType:'json',
                success:function(data){
                    productvm.datas = data;
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

        }
        })
});
