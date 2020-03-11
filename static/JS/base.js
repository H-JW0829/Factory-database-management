$(function () {
    $('#bs-example-navbar-collapse-1>ul>li').click(function () {
        $(this).addClass('active').siblings('li').removeClass('active');
    })
});