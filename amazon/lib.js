class GermanAddrChecker {
    checkZipCode(zip) {
        var reg = /^[0-9]{5}$/;
        if(reg.test(zip)){
            return true;
        }else {
            return false;
        }
    }
    // Example: Muster Straße 123a
    checkStreet(street) {
        var reg = /^([A-Za-zäößüÄÜÖéÉèÈàÀùÙâÂêÊîÎôÔûÛïÏëËüÜçÇæœ\s.,-]+)([\s\d-/,]+[a-zA-Z]?)$/
        if(reg.test(street)){
            return true;
        } else {
            return false;
        }    
    }

    // Example: Muster Straße | 123a
    splitStreet(street) {
        if (!this.checkStreet(street)) {
            return null;
        } else {
            return [RegExp.$1, RegExp.$2];
        }
    }
    
}


function highlight(keyword, targetDom, color) {
    if (keyword != null ) {
        keyword = keyword.replace("&", "&amp;")
        var content = targetDom.innerHTML;
        var arr = content.split(keyword);
        if (arr.length == 2 ) {
            targetDom.innerHTML = arr.join(`<span style="background:${color};">${keyword}</span>`);
        }
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

//Quote: https://stackoverflow.com/a/61511955
// Wait for element to exist
function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelector(selector));
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}

// Json to form
function convertJsonToForm(data) {
    ans = Object.keys(data).map(function(k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(data[k])
    }).join('&')
    return ans
}

var Carriers = {
    createGlsLabel: function(url, data, callback) {
        console.log("createGlsLabel", data);
        GM_xmlhttpRequest({
            method: "post",
            url: url,
            data:  convertJsonToForm(data),
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            onload: function(res) {
                var glswin = window.open ("", "GLS Label", "location=no,status=no,scrollvars=no,width=800,height=900");
                glswin.document.write(res.responseText);
                if (callback) {
                    var trackId = glswin.document.getElementById("trackId-1").textContent;
                    callback(trackId.replace("|", "").trim())
                }
            },
            onerror: function(res) {
                console.log(res.responseText);
                Toast("Error", 1000)
            }

        })
    }
}
