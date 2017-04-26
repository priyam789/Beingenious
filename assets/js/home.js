$(function() {
    var canvas = document.getElementById("cvs"),
        ctx = canvas.getContext("2d");

    // var 

    var width = $(document).width();
    var height = 624;

    var width = document.getElementById('top1').offsetWidth;

    canvas.width = width;
    canvas.height = height;

    var background = new Image();
    background.src = "/assets/images/home.jpg";
    
    // initialize();

    // background.onload = function(){

    //     redraw();
    // }


    // // function 


    // function initialize() {
    //     // Register an event listener to
    //     // call the resizeCanvas() function each time 
    //     // the window is resized.
    //     window.addEventListener('resize', resizeCanvas, false);
        
    //     // Draw canvas border for the first time.
    //     resizeCanvas();
    // }

    // function resizeCanvas() {
    //     // ctx.canvas.width = document.getElementById('top1').offsetWidth;
    //     // ctx.canvas.height = height;
    //     // console.log(canvas.width);
    //     $('top1').resizeCanvas(document.getElementById('top1').offsetWidth, height);
    //     redraw();
    // }

    syncResize();

    function redraw() {

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

    function syncResize() {
        // get the precentage of height and width  of the cavas based on the height and width of the window
        getPercentageOfWindow = function() {
            var viewportSize = getViewportSize();
            var canvasSize = getCanvastSize();
            return {
                x: canvasSize.width / (viewportSize.width - 10),
                y: canvasSize.height / (viewportSize.height - 10)
            };
        };
        //get the context of the canvas 
        getCanvasContext = function() {
            return $("#cvs")[0].getContext('2d');
        };
        // get viewport size
        getViewportSize = function() {
            return {
                height: 624,
                width: window.innerWidth
            };
        };
        // get canvas size
        getCanvastSize = function() {
            var ctx = getCanvasContext();
            return {
                height: ctx.canvas.height,
                width: ctx.canvas.width
            };
        };
        // update canvas size
        updateSizes = function() {
            var viewportSize = getViewportSize();
            // console.log(viewportSize);
            var ctx = getCanvasContext();
            ctx.canvas.height = viewportSize.height * percentage.y;
            ctx.canvas.width = viewportSize.width * percentage.x;
            console.log(ctx.canvas.width);
        };
        var percentage = getPercentageOfWindow();
        
        adapt = function(){
            updateSizes();
            redraw();
        };

        window.onload = adapt;
        window.onresize = adapt;
    }
});
