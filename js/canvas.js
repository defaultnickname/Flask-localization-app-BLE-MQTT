document.getScroll = function () {
    if (window.pageYOffset != undefined) {
        return [pageXOffset, pageYOffset];
    } else {
        var sx, sy, d = document,
            r = d.documentElement,
            b = d.body;
        sx = r.scrollLeft || b.scrollLeft || 0;
        sy = r.scrollTop || b.scrollTop || 0;
        return [sx, sy];
    }
}


function dra() {
    // get canvas related references
    var bg = document.getElementById("bg");
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    var BB = canvas.getBoundingClientRect();
    var offsetX = BB.left;
    var offsetY = BB.top;
    var img = new Image();
    var anchors = [];
    var targets = [];

    for (var i =0; i <10; i++){
        createTarget(0,0)
    }


// listen for mouse events
    canvas.onmousedown = myDown;
    canvas.onmouseup = myUp;
    canvas.onmousemove = myMove;
    setbg('https://i.imgur.com/CsMeCOa.png')


    function setbg(path) {
        img.onload = function () {
            bg.style.backgroundImage = 'url(' + img.src + ')'
            bg.width = this.width;
            bg.height = this.height;
            canvas.width = this.width;
            canvas.height = this.height;
            cbg = document.getElementById("CanvAndBG");


            cbg.style.height = JSON.stringify(this.height) + 'px';


            draw();
        }
        img.src = path
    }

    dra.setbg = setbg;


    function getAllRectangles() {

        return anchors;
    }

    dra.getAllRectangles = getAllRectangles;

     function getAllTargets() {

        return targets;
    }

    dra.getAllTargets = getAllTargets;

    function createAnchor(x, y) {
        anchors.push({x: x, y: y, width: 15, height: 15, fill: '#E32636', isDragging: false});  //TO DO : check if you want to push same thing more times. If yes - ignore
        draw();
    }dra.createAnchor = createAnchor;

    function createTarget(x,y){
        targets.push({x: x, y: y, width: 15, height: 15, fill: '#0000ff'});

    }dra.createTarget = createTarget;

    function updateTarget(id,x,y){
        let thyng = targets[id];
        thyng.x = x;
        thyng.y = y;
        draw();
    }dra.updateTarget = updateTarget;


    function deleteRectangle() {
        anchors.pop();
        draw()
    }dra.deleteRectangle = deleteRectangle;




    function rect(r) {
        ctx.fillStyle = r.fill;
        ctx.fillRect(r.x, r.y, r.width, r.height);
    }


// drag related variables
    var dragok = false;
    var startX;
    var startY;

// an array of objects that define different shapes

// define 2 rectangles


    function clear() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

// redraw the scene
    function draw() {
        clear();
        // redraw each shape in the shapes[] array
        for (var i = 0; i < anchors.length; i++) {
            // decide if the shape is a rect or circle
            // (it's a rect if it has a width property)
                rect(anchors[i]);

        }

         for (var i = 0; i < targets.length; i++) {
            // decide if the shape is a rect or circle
            // (it's a rect if it has a width property)
                rect(targets[i]);

        }
    }


// handle mousedown events
    function myDown(e) {
        console.log(getAllRectangles())
        console.log(getAllTargets())
        let [ScrollLeft, ScrollTop] = document.getScroll();
        // tell the browser we're handling this mouse event
        e.preventDefault();
        e.stopPropagation();

        // get the current mouse position
        var mx = parseInt(e.clientX - offsetX + ScrollLeft);
        var my = parseInt(e.clientY - offsetY + ScrollTop);

        // test each shape to see if mouse is inside
        dragok = false;
        for (var i = 0; i < anchors.length; i++) {
            var s = anchors[i];
            // decide if the shape is a rect or circle
            if (s.width) {
                // test if the mouse is inside this rect
                if (mx > s.x && mx < s.x + s.width && my > s.y && my < s.y + s.height) {
                    // if yes, set that rects isDragging=true
                    dragok = true;
                    s.isDragging = true;
                }
            } else {
                var dx = s.x - mx;
                var dy = s.y - my;
                // test if the mouse is inside this circle
                if (dx * dx + dy * dy < s.r * s.r) {
                    dragok = true;
                    s.isDragging = true;
                }
            }
        }
        // save the current mouse position
        startX = mx;
        startY = my;
    }


// handle mouseup events
    function myUp(e) {
        // tell the browser we're handling this mouse event

        e.preventDefault();
        e.stopPropagation();

        // clear all the dragging flags
        dragok = false;
        for (var i = 0; i < anchors.length; i++) {
            anchors[i].isDragging = false;
        }

    }


// handle mouse moves
    function myMove(e) {
        let [ScrollLeft, ScrollTop] = document.getScroll();
        // if we're dragging anything...
        if (dragok) {

            // tell the browser we're handling this mouse event
            e.preventDefault();
            e.stopPropagation();

            // get the current mouse position
            var mx = parseInt(e.clientX - offsetX + ScrollLeft);
            var my = parseInt(e.clientY - offsetY + ScrollTop);


            // calculate the distance the mouse has moved
            // since the last mousemove
            var dx = mx - startX;
            var dy = my - startY;

            // move each rect that isDragging
            // by the distance the mouse has moved
            // since the last mousemove
            for (var i = 0; i < anchors.length; i++) {
                var s = anchors[i];
                if (s.isDragging) {
                    s.x += dx;
                    s.y += dy;
                }
            }

            // redraw the scene with the new rect positions
            draw();

            // reset the starting mouse position for the next mousemove
            startX = mx;
            startY = my;
        }
    }
}
