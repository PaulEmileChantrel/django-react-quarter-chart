

function displayWeek(index) {

    if (index == 0) { 
        return 'This week';
    }
    else if (index == 1) { 
        return 'Next week';
    }
    else {
        return 'In '+ index+ ' weeks';
    }

}

export default displayWeek;