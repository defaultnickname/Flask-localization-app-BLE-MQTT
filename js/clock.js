


function clock() {


        var dzisiaj = new Date();

        var hours = dzisiaj.getHours();
        var mins = ('0'+ dzisiaj.getMinutes()).slice(-2);
        var seconds = ('0'+ dzisiaj.getSeconds()).slice(-2);

        document.getElementById("time").innerHTML = hours + ':' + mins + ':' + seconds
        setTimeout("clock()",1000)
    }