

function displayWeek(index) {

    if (index == 0) { 
        return 'This Week :';
    }
    else if (index == 1) { 
        return 'Next Week :';
    }
    else {
        return 'In '+ index+ ' Weeks : ';
    }

}

export default displayWeek;