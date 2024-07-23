

console.log("app2: AmazonOrderListApplication")

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
                var linkConfirmShipment = this.surface.setConfirmShipmentLink(orders);   
                var linkPackShipment = this.surface.setPackSlipLink(orders);
                window.open(linkConfirmShipment, '_blank');
                window.open(linkPackShipment, '_blank').focus();
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
        this.link_packSlips = "https://sellercentral.amazon.de/orders/packing-slip?orderIds=";
    }
    // Create Button of bulk confirming orders.
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
    // Get a list of seleted orders.
    getSelectedOrderNumbers() {
        var listOrder = [];        
        // Get orders number from table;
        $("#orders-table > tbody > tr").each((index) => {
            const a = $(`#orders-table > tbody > tr:nth-child(${index+1}) > td:nth-child(3) > div > div.cell-body-title > a`);
            var odn = a.text().trim();
            var asin = $(`#orders-table > tbody > tr:nth-child(${index+1}) > td:nth-child(5) > div > div > div:nth-child(2) > div > b`);
            var asin = asin.text().trim();
            listOrder.push({"orderNumber": odn, "asin": asin});
        });
        // Sort orders by asin
        listOrder.sort((a, b) => {
            if(a.asin > b.asin) return 1;
            if(a.asin < b.asin) return -1;
            return 0;
        })
        // Get selected orders
        var link = $('span[data-test-id="ab-bulk-buy-shipping"] > span > a').attr('href');
        var selectedOrders = link.split(';');
        selectedOrders = selectedOrders.filter(o => o !== "" && o !== null);
        selectedOrders[0] = selectedOrders[0].split("=")[1];
        // Get selected orders sort by asin
        var res = listOrder.map(o => o.orderNumber)
                            .filter(o =>selectedOrders.includes(o));
        return res;
    }

    setConfirmShipmentLink(orders) {
        const link = this.link_confirmShipments + "/" + orders.join(";") + ";";
        console.log(link);
        return link
    }

    setPackSlipLink(orders) {
        const link = this.link_packSlips  + orders.join(";") + ";";
        console.log(link);
        return link;
    }

}

function insertConfirmShipmentToLinks() {  
    // Insert link to Confirm-Shipment-Button
    $("#bulk-confirm-orders-table > tbody > tr").each((index) => {
        var tag = $(`#bulk-confirm-orders-table > tbody > tr:nth-child(${index+1}) > td:nth-child(1) > div > div.cell-body-title > a`)
        var a = tag.attr("href");
        tag.attr("href", a+"/confirm-shipment")
    })
    
}