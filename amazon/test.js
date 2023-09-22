// ^([a-zäöüß\s\d.,-]+?)\s*([\d\s]+(?:\s?[-|+/]\s?\d+)?\s*[a-z]?)?\s*(\d{5})\s*(.+)?$

function checkStreet(street) {
    var reg = /^([A-Za-zäößüÄÜÖ\s.,-]+)\s([\d]+[a-zA-Z]?)$/
    console.log(reg.test(street), street);
    console.log( RegExp.$1, RegExp.$2);
    // console.log(street.replace(reg, "$2, $1"));

}

var street = 'Gewerbegebiet Ziesegrund 11'
checkStreet(street);
street = 'Sonnenwiechser Str. 42a'
checkStreet(street);
street = 'Große Straße  42a'
checkStreet(street);
street = 'Große Straße 42'
checkStreet(street);
street = 'Große Str. 42'
checkStreet(street);
street = 'Großestr. 42'
checkStreet(street);
street = 'Großestr. 42a'
checkStreet(street);
street = 'Großestr.'
checkStreet(street);
street = 'Großestr'
checkStreet(street);
street = '23'
checkStreet(street);
street = '23a'
checkStreet(street);
street = 'Heidbergstrasse 53'
checkStreet(street);