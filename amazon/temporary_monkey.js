// ==UserScript==
// @name         Amazon Order Extractor
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  try to take over the world!
// @author       Yixing
// @match        https://sellercentral-europe.amazon.com/orders-v3/order/*
// @match        https://sellercentral.amazon.de/orders-v3/order/*
// @require      https://raw.githubusercontent.com/yixinglin/scripts-ecommerce/main/amazon/order.js
// @require      https://raw.githubusercontent.com/yixinglin/scripts-ecommerce/main/amazon/lib.js
// @require      https://raw.githubusercontent.com/yixinglin/scripts-ecommerce/main/amazon/app.js
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @run-at       document-end
// @grant        unsafeWindow
// @grant        GM_log
// @grant        GM_setClipboard
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// ==/UserScript==


var GLS_HOST;
const MODE = 3;
switch (MODE) {
    case 1: GLS_HOST = 'http://test.example-test.com'; // Testing
        break;
    case 2: GLS_HOST = 'http://stage.example-stage.com'; // Staging
        break;
    case 3: GLS_HOST = 'http://prod.example.com'; // production
        break;
}

(() => {
    'use strict';
    console.log("start");
    const app = new AmazonOrderApplication(document, GLS_HOST);
    app.init();
})();
