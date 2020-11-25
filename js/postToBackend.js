


function PostToBackend(){
    var buff = dra.getAllRectangles()

    for (const element of buff) {
        delete element['fill'];
        delete element['height'];
        delete element['isDragging'];
        delete element['width'];
}

    //combine anchor data and checkbox state as a flag for python scheduler
    var obj = { anchor: buff, checkbox: true };

    console.log("Here I send rectangles data by AJAX to backend",buff)

    fetch(`${window.origin}/home`, {
        method:'POST',
        credentials: "include",
        body: JSON.stringify(obj),
        cache: "no-cache",
        headers :new Headers({
            'content-type': "application/json"})
    })

}


