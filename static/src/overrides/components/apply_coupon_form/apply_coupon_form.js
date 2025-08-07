import { Component, useState } from "@odoo/owl";


export class OfferCouponForm extends Component {
    static template = "subscription_fields_website.applyCouponForm";
    
    setup(){
        console.log("Empezando el apply coupon form");
        
        const state = {
            code: "",
        }

        this.state = useState(state);
    }
}