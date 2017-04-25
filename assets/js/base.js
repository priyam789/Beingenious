function drawHead(){
	var canvas = document.getElementById('head_canvas');



	var ctx = canvas.getContext('2d');
	ctx.font = 'italic 18px Arial';
	ctx.textAlign = 'center';
	ctx. textBaseline = 'middle';

	console.log("width = " + canvas.width.toString());
	ctx.fillStyle = "#052020";
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	ctx.fillStyle = 'red';  // a color name or by using rgb/rgba/hex values

	var head_text = 'Beingenious';
	text_width = ctx.measureText(head_text).width;
	ctx.fillText(head_text, text_width, 10); // text and position
}