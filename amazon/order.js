
function testAlert() {
    alert("testAAA");
}

class GermanLike {
    constructor(dom) {
        // this.countryMap = {"Amazon.de": "de", "Amazon.fr": "fr", "Amazon.it": "it", "Amazon.es": "es"};
        this.countryMap = {"Amazon.de": "de"};
        this.dom = dom;
    }

    parse() {
        var dom1 = this.dom.querySelector('div[data-test-id="shipping-section-buyer-address"]'); // Shipment
        var lines = dom1.childNodes
        var dom2 = this.dom.querySelector('table.a-keyvalue'); // orderLines
        var dom3 = this.dom.querySelector('span[data-test-id="order-summary-sales-channel-value"]');   // Channel
        var pureLines = [];
        for ( var i=0; i<lines.length; i++ ) {
            pureLines.push(lines[i].innerText.trim());
        }
        pureLines.reverse();
        // data preprocessing
        if (!checkZipCode(pureLines[0]) && checkZipCode(pureLines[1])) {
            pureLines.shift() // delete country line.
        }

        var ele = pureLines[1]
        if (ele.indexOf(",") != -1) {
            pureLines.splice(1, 0, null)
        }
        if (pureLines.length > 6) {
            alert("Items > 6");
            throw new Error('Items > 6!');
        }
        console.log(pureLines);
        
        // zip, [state], city, street, company, name
        var shipment = {};
        const channel = dom3.textContent.trim();  
        shipment.country = this.countryMap[channel];
        if (shipment.country == undefined) {
            throw new Error(`Country not in the whitelist: [${Object.keys(this.countryMap)}]`);
        }

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

        if (pureLines.length == 5) {
            shipment.name1 = pureLines[4];
            shipment.name2 = "";
            shipment.name3 = "";
        } else if (pureLines.length == 6) {
            shipment.name1 = pureLines[4];
            shipment.name2 = pureLines[5];
            shipment.name3 = "";
        }
        shipment.phone = this.dom.querySelector('span[data-test-id="shipping-section-phone"]').textContent;
        shipment.email = "";
        shipment.pages = 1;
        // const quantity = dom2.querySelectorAll('td')[4].innerText;
        // const note = dom2.querySelectorAll("div.product-name-column-word-wrap-break-all")[1].innerText
        // shipment.note = quantity + note.replace("SKU", "").replace(":", "x").trim();
        shipment.note = ""
        shipment.orderNumber = this.dom.querySelector('span[data-test-id="order-id-value"]').textContent;
        
        highlight(shipment.name1, dom1, 'yellow');
        highlight(shipment.name2, dom1, '#FFD700');
        highlight(shipment.name3, dom1), '#EEB422';
        highlight(shipment.city, dom1, '#BEBEBE');
        highlight(shipment.zip, dom1, '#FFDEAD');
        highlight(shipment.street, dom1, '#87CEEB');
        highlight(shipment.houseNumber, dom1, '#54FF9F');
        highlight(shipment.state, dom1, '#F4A460');
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
        // const ele = '<span data-test-id="clipboard-button" class="a-button"><span class="a-button-inner"><input class="a-button-input" type="submit" value="复制到剪切板"><span class="a-button-text" aria-hidden="true">复制到剪切板</span></span></span>'
        const ele = '<span class="a-button-inner"><input class="a-button-input" type="submit" value="复制客户信息"><span class="a-button-text" aria-hidden="true">复制客户信息</span></span>'
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




