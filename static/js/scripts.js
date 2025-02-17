// Function to toggle the sidebar
function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("slide-in");
}

// Function to redirect to order details
function redirectToOrderDetails(event) {
    event.preventDefault();
    var orderId = document.getElementById("order_id").value;
    if (orderId) {
        window.location.href = orderDetailsUrl + orderId;
    }
}

// Function to redirect to location-based search
function redirectToLocation(event) {
    event.preventDefault();
    var location = document.getElementById("location").value;
    if (location) {
        window.location.href = locationUrl + "?location=" + location;
    }
}

// Function to open a tab
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Function to redirect to analysis
function redirectToAnalysis(event) {
    event.preventDefault();
    var startDate = document.getElementById("start_date").value;
    var endDate = document.getElementById("end_date").value;
    var url = productDetailUrl + "?start_date=" + startDate + "&end_date=" + endDate;
    window.location.href = url;
}