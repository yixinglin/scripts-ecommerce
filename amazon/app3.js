
console.log("App3: Ebay Order Application");

class EbayOrderApp {

    constructor(gls_host) {        
        this.gls_host = gls_host;
        this.findGlsButton = () => document.querySelector("#tm-gls");
        this.findMoreInformationButton = () => document.querySelector("div.item-specifics button");
    }

    init() {
        console.log("App3: Initialized");
        waitForElm('div.shipping-info')
        .then(() => {
            console.log("App3: Found order details header");
            this.#addButtonTo("div.shipping-info div.line-actions",
                "tm-extract",
                "Extract[1]", () => this.onHandleExtractButtonClick(),
            );

            this.#addButtonTo("div.shipping-info div.line-actions",
                "tm-gls",
                "GLS[2]", () => this.onHandleGlsButtonClick(),
            );
            var btn = this.findGlsButton();
            btn.style.display  = "none";   
            this.#clickOnMoreInformationButton();           
        })
    }

    #addButtonTo(selector, id, name, callback) {
        // div.shipping-info div.line-actions
        const container = document.querySelector(selector);
        const button = document.createElement("button");
        // add class to button for styling
        button.classList.add("default-action", "btn", "btn--secondary");
        // add background color to button for styling
        button.style.backgroundColor = "pink";
        button.innerText = name;
        // Add id to button 
        button.id = id;
        button.addEventListener("click", callback);
        container.appendChild(button);          
    }

    #addTextTo(selector, text, color) {
        const container = document.querySelector(selector);
        const p = document.createElement("p");
        p.innerText = text;
        p.style.color = color;
        container.appendChild(p);
    }

    onHandleExtractButtonClick() {
        // alert("Extract button clicked");
        // display gls button
        try {
            const shipment = this.#extractOrderDetailsV1();
            // console.log(shipment);
            var btn = this.findGlsButton();
            btn.style.display  = "";
            btn.disabled = false;
            this.shipment = shipment;
        } catch (error) {
            console.error(error);
            alert(error);
        }        
        
    }


    onHandleGlsButtonClick() {
        const shipment = this.shipment;
        // console.log(shipment);                
        this.#createGlsLabel(shipment);
        this.findGlsButton().disabled = true;
    }

    #clickOnMoreInformationButton() {
        const btn = this.findMoreInformationButton();
        if (btn) {
            btn.click();    
        }
    }

    #extractOrderDetailsV1() {
        var shipment = {};
        // shipment.name1 = document.querySelector('[id^="nid-"][id$="-5"]').innerText;;
        shipment.name1 = this.#getFieldByTooltip("Namen kopieren");
        shipment.name2 = "";
        shipment.name3 = "";
        shipment.city = this.#getFieldByTooltip("Ort kopieren");
        shipment.state= "";
        shipment.zip = this.#getFieldByTooltip("PLZ kopieren");
        shipment.country = this.#getFieldByTooltip("Land/Region kopieren");
        shipment.street = this.#getFieldByTooltip("Straße kopieren");
        shipment.houseNumber = "";
        shipment.phone = this.#getFieldByTooltip("In Zwischenablage kopieren");
        shipment.email = "";
        shipment.pages = 1;
        shipment.note = "";
        shipment.orderNumber = document.querySelector('div.order-info div.info-item dd').innerText;
        if (shipment.country === "Germany" || shipment.country === "Deutschland") {
            shipment.country = "DE";
        } else {            
            throw new Error("Only German orders are supported");
        }
        return shipment;
    }

    #createGlsLabel(shipment) {
        console.log("App3: Creating GLS label", shipment);
        Carriers.createGlsLabel(this.gls_host+'/gls/label', shipment, (trackId) => {
            console.log(trackId);
            this.#addTextTo("div.shipping-info div.line-actions", "Tracking Number: " + trackId, 'red');
        });
    }

    #getFieldByTooltip(text) {
        const tooltips = document.querySelectorAll('.tooltip__mask');
        for (let i = 0; i < tooltips.length; i++) {
            const tooltip = tooltips[i];
            const tooltipText = tooltip.innerText.trim();
            if (tooltipText === text) {
                const parent = tooltip.parentElement.parentElement;                
                return parent.innerText.trim();
            }
        }
        throw new Error("Could not find field with tooltip " + text);
    }
}