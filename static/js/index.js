function navMenu() {
    var x = document.getElementById("navbar__mobile");
    if (x.className === "navbar__mobile") {
      x.className += " on";
    } else {
      x.className = "navbar__mobile";
    }
  }