
function testAlert() {
    alert("testAAA");
}

class GermanLike {
    constructor(dom) {
        this.dom = dom.querySelector('div[data-test-id="shipping-section-buyer-address"]');
    }

    parse() {
        const lines = this.dom.childNodes;
        var pureLines = [];
        for ( var i=0; i<lines.length; i++ ) {
            pureLines.push(lines[i].innerText.trim());
        }
        pureLines.reverse();
        const ele = pureLines[1]
        if (ele.indexOf(",") != -1) {
            pureLines.splice(1, 0, null)
        }
        console.log(pureLines);
        
        // zip, state, city, street, company, name
        var shipment = {};
        const zip = pureLines[0];
        if (!checkZipCode(zip)) {
            throw new Error('ZipCode unrecognized!');
        } else {
            shipment.zip = zip;
        }
    
        shipment.state = pureLines[1];
        shipment.city = pureLines[2].replace(',', '');
        
        const street = pureLines[3];
        if (!checkStreet(street)) {
            throw new Error('Street unrecognized!');
        } else {
            const st = splitStreet(street);
            shipment.street = st[0];
            shipment.houseNumber = st[1];
        }   

        return shipment;
    }

}

