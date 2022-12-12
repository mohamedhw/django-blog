let upButton = document.getElementById('up');

window.onscroll = () => {
    if (window.scrollY >= window.innerHeight/5){
        upButton.style.display = "block";
    }else{
        upButton.style.display = "none";
    }
};



function topWindo(){
    document.documentElement.scrollTop = 0;
};
