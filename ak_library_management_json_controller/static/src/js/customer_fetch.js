/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
console.log(">>>>>>>>>document.getElementById('email')")

publicWidget.registry.customerFetchDetails = publicWidget.Widget.extend({
    selector: '.fetchdata',
    events: {
        'click #submitFetchData': '_onClickfetchdata1',
    },

    async _onClickfetchdata1() {
        console.log(this)
        let email = $('#email11').val()
        let resultdiv = document.getElementById('resultdiv')
        const CustomerData = await rpc("/action_send_mail", {values : email});
        console.log(CustomerData)
        if (CustomerData.length != 0) {
            const rows = CustomerData.map(c => `
                <tr>
                    <td>${c.customer_name}</td>
                    <td>${c.customer_phone}</td>
                </tr>
            `).join('');

            resultdiv.innerHTML = `
                <table class="table table-bordered o_table">
                    <thead>
                        <tr>
                            <td>Name</td>
                            <td>Phone</td>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows}
                    </tbody>
                </table>`;
        }
        else{
        resultdiv.innerHTML = `
            <div style="border:1px solid #ccc; padding:10px; border-radius:8px; color: red;">
                <p><strong>No Customer Found With the relative email address</strong></p>
            </div>`;
        }
        return resultdiv;
        console.log(CustomerData)
    }
});
