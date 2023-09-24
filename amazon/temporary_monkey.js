// ==UserScript==
// @name         Amazon Order Extractor
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Yixing
// @match        file:///F:/shared/amazon/example*.*
// @match        https://sellercentral.amazon.de/orders-v3/order/*
// @require      file://G:\hansagt\tampermonkey\scripts-ecommerce\amazon\order.js
// @require      file://G:\hansagt\tampermonkey\scripts-ecommerce\amazon\lib.js
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @run-at       document-end
// @grant        unsafeWindow
// @grant        GM_log
// @grant        GM_setClipboard
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// ==/UserScript==

const GLS_HOST = 'http://127.0.0.1:5000';

(() => {
    'use strict';
    const DELAY_SEC = 1000;
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
    Carriers.createGlsLabel(GLS_HOST+'/gls/label', shipment);
}







