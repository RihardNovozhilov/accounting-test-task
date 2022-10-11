odoo.define('website_sale.additional_image_field', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var core = require('web.core');
    var FieldBinaryImage = basic_fields.FieldBinaryImage;
    var fieldRegistry = require('web.field_registry');


    var AdditionalImage = FieldBinaryImage.extend({

        events: _.extend({}, FieldBinaryImage.prototype.events, {
            'mouseover .img-fluid': '_changeImage',
            'mouseout .img-fluid': '_originalImage',
        }),

        _changeImage: function (event) {
            if (!this.recordData.active_additional_image)
                return;
            event.target.src = "/web/image?model=product.template&id=" + this.recordData.id + "&field=additional_image";
        },

        _originalImage: function (event) {
            if (!this.recordData.active_additional_image)
                return;
            event.target.src = "/web/image?model=product.template&id=" + this.recordData.id + "&field=image_1920";
        },


    });

    fieldRegistry.add('additional_image', AdditionalImage);

    return {
        AdditionalImage: AdditionalImage,
    };

})
