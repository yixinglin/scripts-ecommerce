
class AmazonOrderApplication {

    constructor(dom, gls_host) {
        this.dom = dom;
        this.gls_host = gls_host;
    }

    init() {
        console.log("init");
        waitForElm('div[data-test-id="order-details-header-action-buttons"]')
        .then((elm) => {
            console.log('Element is ready');
            this.parser = new GermanLike(this.dom);
            this.surface = new OrderPageSurface(this.dom);
            const recognitionButton = this.surface.addButtonRecognizeCustomerInfo();
            recognitionButton.addEventListener('click', () => {
                this.onClickParseFromSurfaceButton();
            })
        });
    }

    // 1. Button for parsing info on the webpage.
    onClickParseFromSurfaceButton() {
        var shipment = null;
        try {
            shipment = this.parser.parseFromWebSurface();
            if ( shipment != undefined ) {
                const info = JSON.stringify(shipment, null, 2);
                this.surface.addButtonGLSParcelLabel();
                var glsBtn = this.dom.querySelector('span[data-test-id="gls-button"] > span > input');
                glsBtn.addEventListener('click', () => {
                    this.onClickGLSButton(shipment);
                    glsBtn.disabled = true;
    
                })
            }
        } catch(err) {
            alert(err);
            const oneClickButton = this.surface.addButtonOneClickGls();
            oneClickButton.addEventListener('click', () => {
                this.onClickOneClickButton();
            })
        }
        console.log(shipment);
    }
    
    // 2. Gls button to create parcel labels.
    onClickGLSButton(shipment) {
        console.log(shipment);
        this.createGlsLabel(shipment)
    }

    // 3. Apply Amazon API to create GLS label.
    onClickOneClickButton() {
        var shipment = null;
        AmazonApi.fetchShipmentFromApi(this.parser.getOrderNumber())
        .then(res => {
            var shipment = JSON.parse(res);
            shipment = this.parser.parseApiData(shipment);
            if (shipment != undefined) {
                this.createGlsLabel(shipment)
            }
        }).catch(err => {
            alert(err);
        });
        console.log(shipment);
    }

    createGlsLabel(shipment) {
        Carriers.createGlsLabel(this.gls_host+'/gls/label', shipment, (trackId) => {
            console.log(trackId);
            let trackInput = this.dom.querySelector('input[data-test-id="text-input-tracking-id"]');
            if (trackInput) {
                setValueToInputElm(trackInput, trackId);
            }
        });
    }

}


// Create Widgets on the website.
class OrderPageSurface {
    constructor(dom) {
        this.dom = dom;
        this.buttonBar = this.dom.querySelector('div[data-test-id="order-details-header-action-buttons"]');
        this.recognitionButton = null;
        this.glsBtn = null;
    }

    addButtonRecognizeCustomerInfo() {
        const ele = '<span class="a-button-inner">' +
            '<input class="a-button-input" type="submit" value="识别地址 [1]">' +
            '<span class="a-button-text" aria-hidden="true">识别地址 [1]</span></span>'
        const ivBtn = this.buttonBar.querySelector('span[data-test-id="manage-idu-invoice-button"]'); // First button
        this.recognitionButton = ivBtn.cloneNode(true);      // Create a new button
        this.recognitionButton.setAttribute("data-test-id", "recognize-button");  // Set button id
        this.recognitionButton.innerHTML = ele;          // Set button content
        this.buttonBar.insertBefore(this.recognitionButton, ivBtn);  // Place button at the first position
        return this.recognitionButton;
    }

    addButtonGLSParcelLabel() {
        if (this.glsBtn != null) {
            return this.glsBtn;
        } else {
            const ele = '<span class="a-button-inner"><input class="a-button-input" type="submit" value="GLS [2]"><span class="a-button-text" aria-hidden="true">GLS [2]</span></span>'
            this.glsBtn = this.recognitionButton.cloneNode(true);      // Create a new button
            this.glsBtn.setAttribute("data-test-id", "gls-button");  // Set button id
            this.glsBtn.innerHTML = ele;
            this.buttonBar.insertBefore(this.glsBtn, this.recognitionButton);
            return this.glsBtn;
        }
    }

    addButtonOneClickGls() {
        if (this.oneClickButton != null) {
            return this.oneClickButton;
        } else {
            const ele = '<span class="a-button-inner"><input class="a-button-input" type="submit" value="直接打印 [3]"><span class="a-button-text" aria-hidden="true">直接打印 [3]</span></span>'
            const rgBtn = this.recognitionButton.cloneNode(true); 
            this.oneClickButton = rgBtn.cloneNode(true);      // Create a new button
            this.oneClickButton.setAttribute("data-test-id", "api-button");  // Set button id
            this.oneClickButton.innerHTML = ele;          // Set button content
            this.buttonBar.insertBefore(this.oneClickButton, this.recognitionButton);  // Place button at the first position
        }
        return this.oneClickButton;
    }

    
}