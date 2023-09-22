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

// Example: Muster Straße 123a
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

// Example: Muster Straße | 123a
function splitStreet(street) {
    if (!checkStreet(street)) {
        return null;
    } else {
        return [RegExp.$1, RegExp.$2];
    }
}

// Message show up
function Toast(msg, duration){  
    duration=isNaN(duration)?3000:duration;  
    var m = document.createElement('div');  
    m.innerHTML = msg;  
    m.style.cssText="font-size: .32rem;color: rgb(255, 255, 255);background-color: rgba(0, 0, 0, 0.6);padding: 10px 15px;margin: 0 0 0 -60px;border-radius: 4px;position: fixed;    top: 50%;left: 50%;width: 430px;text-align: center;";
    document.body.appendChild(m);  
    setTimeout(function() {  
        var d = 0.5;
        m.style.opacity = '0';  
        setTimeout(function() { document.body.removeChild(m) }, d * 1000);  
    }, duration);  
}  