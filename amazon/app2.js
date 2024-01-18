

console.log("app2 loaded")

class AmazonOrderListApplication {

    constructor(dom) {
        this.dom = dom;
        console.log("AmazonOrderListApplication");
    }

    init() {
        console.log("init");
        waitForElm('span[data-test-id="bulk-print-packingslip"]')
        .then((elm) => {
            console.log('Element is ready1');
            this.surface = new OrderListPageSurface(this.dom);
            this.surface.addButtonBulkConfirmShipmentV2().on("click", () => {
                const orders = this.surface.getSelectedOrderNumbers();   // Order sorted by asin
                var links = this.surface.setConfirmShipmentLink(orders);   
                window.open(links, '_blank').focus();
            })
        });

        waitForElm('span[data-test-id="bulk-confirm-shipment-submit"]')
        .then((elm) => {
            console.log('Element is ready2');
            insertConfirmShipmentToLinks();
        });
    }
}

function copyItem(copyItem, targetItem, callback) {
    $(targetItem).append($(copyItem).clone());
    callback($(targetItem).children(":last-child"));
}

// Create Widgets on the website.
class OrderListPageSurface {
    constructor(dom) {
        this.dom = dom;
        this.confirmShipmentButton = null;   
        this.link_confirmShipments = "https://sellercentral.amazon.de/orders-v3/bulk-confirm-shipment";
    }

    addButtonBulkConfirmShipmentV2() {
        const name = "分类并确认送货[1]";
        const ele = `<span class="a-button-inner"><input class="a-button-input" type="submit" value=${name} aria-labelledby="a-autoid-10-announce"><span class="a-button-text" aria-hidden="true">${name}</span></span>`;

        const csBtn_c = $('span[data-test-id="ab-bulk-confirm-shipment"]');
        const csBtn = csBtn_c.parent();
        this.confirmShipmentButton = csBtn_c.clone().html(ele);
        this.confirmShipmentButton
                .attr("data-test-id", "bulk-confirm-shipment-buttonV2")
                .removeClass()
                .addClass("a-button a-button-enabled myo-bulk-action-button a-button-normal");
        csBtn.after(this.confirmShipmentButton);
        return this.confirmShipmentButton;
    }

    getSelectedOrderNumbers() {
        var listOrder = [];        
        $("#orders-table > tbody > tr").each((index) => {
            const a = $(`#orders-table > tbody > tr:nth-child(${index+1}) > td:nth-child(3) > div > div.cell-body-title > a`);
            var odn = a.text().trim();
            var asin = $(`#orders-table > tbody > tr:nth-child(${index+1}) > td:nth-child(5) > div > div > div:nth-child(2) > div > b`);
            var asin = asin.text().trim();
            listOrder.push({"orderNumber": odn, "asin": asin});
        });

        listOrder.sort((a, b) => {
            if(a.asin > b.asin) return 1;
            if(a.asin < b.asin) return -1;
            return 0;
        })

        return listOrder.map(o => o.orderNumber);
    }

    setConfirmShipmentLink(orders) {
        const link = this.link_confirmShipments + "/" + orders.join(";") + ";";
        console.log(link);
        return link
    }

}

function insertConfirmShipmentToLinks() {  
    $("#bulk-confirm-orders-table > tbody > tr").each((index) => {
        var tag = $(`#bulk-confirm-orders-table > tbody > tr:nth-child(${index}) > td:nth-child(1) > div > div.cell-body-title > a`)
        var a = tag.attr("href");
        tag.attr("href", a+"/confirm-shipment")
        debugger
    })
    
}