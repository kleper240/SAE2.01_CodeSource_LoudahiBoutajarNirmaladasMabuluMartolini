function selectStars(count) {
    const stars = document.getElementsByClassName('star');
    for (let i = 0; i < stars.length; i++) {
        if (i < count) {
            stars[i].classList.add('selected');
        } else {
            stars[i].classList.remove('selected');
        }
    }
    document.getElementById('etoiles').value = count;
}
