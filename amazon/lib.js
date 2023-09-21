function checkZipCode(postalCode) {
    var reg = /^[0-9]{5}$/;
    if(reg.test(postalCode)){
        return true;
    }else if(postalCode==""||postalCode.length==0){
        alert("邮政编码为空");
        return false;
    }else{
        alert("邮政编码解析失败");
        return false;
    }
}

// Example: Muster Strasse 123a
function checkStreet(street) {
    var reg = /^([A-Za-zäößüÄÜÖ\s.,-]+)\s([\d]+[a-zA-Z]?)$/
    if(reg.test(street)){
        return true;
    }else if(street==""||street.length==0){
        alert("街道为空");
        return false;
    }else{
        alert("街道解析失败");
        return false;
    }
}

// Example: Muster Strasse | 123a
function splitStreet(street) {
    if (!checkStreet(street)) {
        return null;
    } else {
        return [RegExp.$1, RegExp.$2];
    }
}
