$(function () {
    $('#show1').css('display','table');
    $('#show2').css('display','none');
    $('#show3').css('display','none');
    $('#a1').click(function () {
        // console.log("click a1");
        $('#show1').css('display','table');
        $('#show2').css('display','none');
        $('#show3').css('display','none');
    });
    $('#a2').click(function () {
        // console.log("click a2");
        $('#show1').css('display','none');
        $('#show2').css('display','table');
        $('#show3').css('display','none');
    });
    $('#a3').click(function () {
        // console.log("click a3");
        $('#show1').css('display','none');
        $('#show2').css('display','none');
        $('#show3').css('display','table');
    });
    
});