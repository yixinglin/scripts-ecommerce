// ==UserScript==
// @name         Amazon Order Extractor
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Yixing
// @match        file:///F:/shared/amazon/example*.*
// @match        https://sellercentral-europe.amazon.com/orders-v3/order/*
// @match        https://sellercentral.amazon.de/orders-v3/order/*
// @require      https://raw.githubusercontent.com/yixinglin/scripts-ecommerce/main/amazon/order.js
// @require      https://raw.githubusercontent.com/yixinglin/scripts-ecommerce/main/amazon/lib.js
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @run-at       document-end
// @grant        unsafeWindow
// @grant        GM_log
// @grant        GM_setClipboard
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// ==/UserScript==

var GLS_HOST;
const MODE = 1;
switch (MODE) {
    case 1: GLS_HOST = 'http://www.example-test.com:5001'; // Testing
        break;
    case 2: GLS_HOST = 'http://www.example-stage.com:5005'; // Staging
        break;
    case 3: GLS_HOST = 'http://www.example-prod.com:5001'; // production
        break;
}

(() => {
    'use strict';

    waitForElm('div[data-test-id="order-details-header-action-buttons"]').then((elm) => {
        console.log('Element is ready');
        const parser = new GermanLike(document);
        const surface = new Surface(document);
        const cbBtn = surface.addButtonCopyToClipboard();
        cbBtn.addEventListener('click', () => {
            onClickCopyCustomerInfo(parser, surface);
        })
    });
})();

function onClickCopyCustomerInfo(parser, surface) {
    var shipment = null;
    GM_setClipboard("");
    try {
        shipment = parser.parse();
        if ( shipment != undefined ) {
            const info = JSON.stringify(shipment, null, 2);
            GM_setClipboard(info); // Copy to clipboard
            GM_setValue("shipment", JSON.stringify(info));
            Toast("已复制客户信息到剪切板！", 1000);
            surface.addButtonGLSParcelLabel();
            var glsBtn = document.querySelector('span[data-test-id="gls-button"] > span > input');
            glsBtn.addEventListener('click', () => {
                onClickGLSButton(shipment);
                glsBtn.disabled = true;

            })
        }
    } catch(err) {
        alert(err);
    }
    console.log(shipment);
}

function onClickGLSButton(shipment) {
    console.log(shipment);
    Carriers.createGlsLabel(GLS_HOST+'/gls/label', shipment, (trackId) => {
        console.log(trackId);
        let trackInput = document.querySelector('input[data-test-id="text-input-tracking-id"]');
        let evt = document.createEvent('HTMLEvents');
        if (trackInput) {
            trackInput.focus();
            trackInput.setAttribute("value", trackId)
            evt.initEvent('input', true, true);
            evt.eventType = 'message';
            trackInput.dispatchEvent(evt);
        }
    });
}
