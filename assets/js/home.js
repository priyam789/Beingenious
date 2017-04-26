$(function() {
    var canvas = document.getElementById("cvs"),
        ctx = canvas.getContext("2d");

    // var 

    var width = $(document).width();
    var height = 624;
    canvas.width = width;
    canvas.height = height;


    var background = new Image();
    background.src = "/assets/images/home.jpg";

    background.onload = function(){
        ctx.drawImage(background,0,0);  
        // ctx.font = "40pt Calibri";
        // ctx.fillText("My TEXT!", 20, 20); 
        var text1 = "Be";
        var text2 = "i";
        var text3 = "nGenious";
        var text4 = "the road to ingenuity ...";
        var text5 = "BeinGenious";

        ctx.font = "40pt Calibri";

        var len1 = ctx.measureText(text1).width;
        var len2 = ctx.measureText(text2).width;
        var len3 = ctx.measureText(text3).width;
        var len4 = ctx.measureText(text4).width;
        var len5 = ctx.measureText(text5).width;

        ctx.fillStyle = "red";
        ctx.fillText(text1, (width - len5)/2, height/4);
        // ctx.fillText(text1, 50, 50)

        ctx.fillStyle = "yellow";
        ctx.fillText(text2, (width - len5)/2 + len1, height/4 - 25);

        ctx.fillStyle = "black";
        ctx.fillText(text3, (width - len5)/2 + len1 + len2, height/4);

        ctx.fillStyle = "white";
        ctx.font = "15pt Calibri";
        ctx.fillText(text4, (width)/2, height/4 + 25);

    }
});

