

function PostToBackend(){

    var buff = dra.getAllRectangles()

    console.log(buff)

    fetch(`${window.origin}/home`, {
        method:'POST',
        credentials: "include",
        body: JSON.stringify(buff),
        cache: "no-cache",
        headers :new Headers({
            'content-type': "application/json"})
    })

}