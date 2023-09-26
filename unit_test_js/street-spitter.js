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
        var pattern1 = /^([A-Za-zäößüÄÜÖ\s.,-]+)([\s\d-/,]+[a-zA-Z]?)$/
        if(pattern1.test(street)){
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

function unit_test_german_addr_splitter() {
    let checker = new GermanAddrChecker()
    const streets = [
        'GewerbeÜgebiet Zies-egruünd 11', 'Gräoße StrÄße 42', 'Gröoße SÖtr. 42', 'Großestr. 42', 'Heidbergstrasse 53',
        'Gewerbegebiet Ziesegrund 11-15', 'Gewerbegebiet Ziesegrund 11/15/18', 'Gewerbegebiet Ziesegrund 11 - 15', 'Gewerbegebiet Ziesegrund 11 / 15 / 18',
        'Gewerbegebiet Ziesegrund 11a - 15a', 'Gewerbegebiet Ziesegrund 11a-15a',
        'Gewerbegebiet Ziesegrund78', 'Gewerbegebiet56',
        'Gewerbegebiet Ziesegrund78a', 'Gewerbegebiet56a',
        'Sonnenwiechser Str. 42a', 'Große Straße  42a', 'Großestr. 42a', 'Großestr 42a',
        'Großestr.', 'Großestr', 'Große str.',
        '23', '23a', "23-45", "23 - 45"  
    ]
    for(s of streets) {
        ans = checker.splitStreet(s);
        if (ans != null) {
            [st, num] = ans;
            console.log(`${s} >> ${st} | ${num}`)
        } else {
            console.log(s, ' -> Fail')
        }
    }
}

unit_test_german_addr_splitter()
