
function testAlert() {
    alert("testAAA");
}

class GermanLike {
    constructor(dom) {
        // this.countryMap = {"Amazon.de": "de", "Amazon.fr": "fr", "Amazon.it": "it", "Amazon.es": "es"};
        this.dom = dom;
        this.countryMap = {"Germany": "de", "Deutschland": "de"};
        this.checkerMap = {
            "Germany": new GermanAddrChecker(), "Deutschland": new GermanAddrChecker(),
        }
        // this.checker = new GermanAddrChecker()
    }

    parse() {
        const ivBtn = document.querySelector('span[data-test-id="manage-idu-invoice-button"]'); // First button
        if (!ivBtn.textContent.includes("invoice") &&  !ivBtn.textContent.includes("Rechnung")) {
            throw new Error("Please switch the web page language to English or German.");
        }

        var dom1 = this.dom.querySelector('div[data-test-id="shipping-section-buyer-address"]'); // Shipment
        var lines = dom1.childNodes
        var dom2 = this.dom.querySelector('table.a-keyvalue'); // orderLines
        // var dom3 = this.dom.querySelector('span[data-test-id="order-summary-sales-channel-value"]');   // Channel
        // const channel = dom3.textContent.trim();  
        var pureLines = [];
        for ( var i=0; i<lines.length; i++ ) {
            pureLines.push(lines[i].innerText.trim());
        }
        pureLines.reverse();
        // Data preprocessing
        const country = pureLines.shift()                           // delete country line.
        const checker = this.checkerMap[country];
        var ele = pureLines[0]
        if (ele.indexOf(",") != -1) {   // if state is not shown
            pureLines.splice(0, 0, ""); // insert state to the array
        }
        if (pureLines.length > 7) {
            throw new Error('Items > 7!');
        }
        console.log(pureLines);
        
        //en-US: [state], city, zip, street, company, name 
        var shipment = {};
        shipment.country = this.countryMap[country];
        if (shipment.country == undefined) {
            throw new Error(`Country not in the whitelist: [${Object.keys(this.countryMap)}]`);
        }

        shipment.state = pureLines[0];
        shipment.city = pureLines[1].replace(',', '');

        const zip = pureLines[2];
        if (!checker.checkZipCode(zip)) {
            throw new Error('ZipCode unrecognized!');
        } else {
            shipment.zip = zip;
        }
    
        const street = pureLines[3];
        if (!checker.checkStreet(street)) {
            throw new Error('Street unrecognized!');
        } else {
            const st = checker.splitStreet(street);
            shipment.street = st[0];
            shipment.houseNumber = st[1];
        }   

        if (pureLines.length == 5) {
            shipment.name1 = pureLines[4];
            shipment.name2 = "";
            shipment.name3 = "";
        } else if (pureLines.length == 6) {
            shipment.name1 = pureLines[4];
            shipment.name2 = pureLines[5];
            shipment.name3 = "";
        } else if (pureLines.length == 7) {
            shipment.name3 = pureLines[4]; // co
            shipment.name1 = pureLines[5]; // company
            shipment.name2 = pureLines[6]; // name
        }
        if (shipment.name2.toLowerCase().includes("gmbh")) {
            [shipment.name1, shipment.name2] = [shipment.name2, shipment.name1];
        }
        // Check DHL parcel
        for(let n of [shipment.name1, shipment.name2, shipment.name3, shipment.street]) {
            var prefix = n.toLowerCase().substring(0, 4);
            if (prefix== 'dhl ' || prefix == 'dhl-' || prefix == 'dhl_') {
                throw new Error('It seems to be a DHL parcel');
            }
        }

        const phoneDom = this.dom.querySelector('span[data-test-id="shipping-section-phone"]');
        shipment.phone = phoneDom!=null? phoneDom.textContent : ""
        shipment.email = "";
        shipment.pages = 1;
        shipment.note = ""
        shipment.orderNumber = this.dom.querySelector('span[data-test-id="order-id-value"]').textContent;
        // const quantity = dom2.querySelectorAll('td')[4].innerText;
        // const note = dom2.querySelectorAll("div.product-name-column-word-wrap-break-all")[1].innerText
        // shipment.note = quantity + note.replace("SKU", "").replace(":", "x").trim();

        const addrDom = this.dom.querySelector('div[data-test-id="shipping-section-buyer-address"]');
        highlight(shipment.name1, addrDom, 'yellow');
        highlight(shipment.name2, addrDom, '#FFD700');
        highlight(shipment.name3, addrDom, '#EEB422');
        highlight(shipment.city, addrDom, '#BEBEBE');
        highlight(shipment.zip, addrDom, '#FFDEAD');
        highlight(shipment.street, addrDom, '#87CEEB');
        highlight(shipment.houseNumber, addrDom, '#54FF9F');
        highlight(shipment.state, addrDom, '#F4A460');
        return shipment;
    }

}

class Surface {
    constructor(dom) {
        this.dom = dom;
        this.buttonBar = this.dom.querySelector('div[data-test-id="order-details-header-action-buttons"]');
        this.cbBtn = null;
        this.glsBtn = null;
    }

    addButtonCopyToClipboard() {
        const ele = '<span class="a-button-inner"><input class="a-button-input" type="submit" value="复制收货地址"><span class="a-button-text" aria-hidden="true">复制收货地址</span></span>'
        const ivBtn = this.buttonBar.querySelector('span[data-test-id="manage-idu-invoice-button"]'); // First button
        this.cbBtn = ivBtn.cloneNode(true);      // Create a new button
        this.cbBtn.setAttribute("data-test-id", "clipboard-button");  // Set button id
        this.cbBtn.innerHTML = ele;          // Set button content
        this.buttonBar.insertBefore(this.cbBtn, ivBtn);  // Place button at the first position
        return this.cbBtn;
    }

    addButtonGLSParcelLabel() {
        if (this.glsBtn != null) {
            return this.glsBtn;
        } else {
            const ele = '<span class="a-button-inner"><input class="a-button-input" type="submit" value="GLS"><span class="a-button-text" aria-hidden="true">GLS</span></span>'
            this.glsBtn = this.cbBtn.cloneNode(true);      // Create a new button
            this.glsBtn.setAttribute("data-test-id", "gls-button");  // Set button id
            this.glsBtn.innerHTML = ele;
            this.buttonBar.insertBefore(this.glsBtn, this.cbBtn);
            return this.glsBtn;
        }
    }

    
}




