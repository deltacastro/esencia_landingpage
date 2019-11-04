window.onload = function(){
    document.getElementById('preloader').style.display = 'none'
}

document.addEventListener('DOMContentLoaded', function () {
    AOS.init()
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
    const backToTopButton = document.querySelector(".scrolltotop");
    window.addEventListener("scroll", function () {
        if (window.pageYOffset > 300) { // Show backToTopButton
            backToTopButton.style.display = "block";
        }
        else { // Hide backToTopButton
            backToTopButton.style.display = "none";
        }
    });
    backToTopButton.addEventListener("click", smoothScrollBackToTop);
    function smoothScrollBackToTop() {
        const targetPosition = 0;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 750;
        let start = null;

        window.requestAnimationFrame(step);

        function step(timestamp) {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            window.scrollTo(0, easeInOutCubic(progress, startPosition, distance, duration));
            if (progress < duration) window.requestAnimationFrame(step);
        }
    }
    function easeInOutCubic(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t * t + b;
        t -= 2;
        return c / 2 * (t * t * t + 2) + b;
    };
});