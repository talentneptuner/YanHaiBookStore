/* 
 * Transform an ugly input into an awesome rating element! 
 * Requires tipi, jQuery and Font Awesome 
 *
 * Author: Federico Ramirez 
 * */
;(function ($, window, document, undefined) {
    'use strict';

    var pluginName = 'rating',
        defaults = {
            // whether or not to display the label under the stars
            showLabel: true,
            // messages for the label under the stars
            messages: [
                '请评分',
                '极差！',
                '较差！',
                '一般！',
                '不错！',
                '极佳！'
            ],
            // error message when the rating is empty
            validationMessage: 'Please rate before you continue',
            // display the widget as inline-block instead of block
            inline: false,
            // the icon from FontAwesome this widget will use
            icon: 'fa-star',
            // colors
            color: '#b08bd7',
            colorHover: '#7d40bc',
            // the size of the icon
            size: '20px'
        };

    // The actual plugin constructor
    function Plugin (element, options) {
        this.element = element;
        this.settings = $.extend({}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    Plugin.prototype = {
        init: function () {
            var $el = $(this.element),
                self = this,
                $container,
                star,
                $message,
                i,
                $starsContainer;

            this.value = $el.val() ? parseInt($el.val(), 10) : 0;

            $el.on('invalid', function (e) {
                e.preventDefault();
                $container.tipi('text', self.settings.validationMessage)
                    .tipi('show');
            });

            // highlight the stars in the container
            function highlightStars(current) {
                var i;

                for(i = 1; i <= 5; i++) {
                    if(i <= current) {
                        $container.find('i[rating-value=' + i + ']').css('color', self.settings.colorHover);
                    } else {
                        $container.find('i[rating-value=' + i + ']').css('color', self.settings.color);
                    }
                }

                if(self.settings.showLabel) {
                    $message.text(self.settings.messages[current]);
                }
            }

            // create DOM elements
            $container = $('<div class="rating-container" />')
            // instantiate tipi on the container
                .tipi();

            if(self.settings.inline) {
                $container.css('display', 'inline-block');
            }
            
            // ... stars
            $starsContainer = $('<div class="stars" />');
            for(i = 1; i <= 5; i++) {
                star = $('<i rating-value="' + i + '" class="fa ' + self.settings.icon + '" />');
                star.css('font-size', self.settings.size);
                $starsContainer.append(star);
            }
            $container.append($starsContainer);

            // ... message
            if(self.settings.showLabel) {
                $message = $('<span />').text(self.settings.messages[0]);
                $container.append($message);
            }

            // bind events
            $container.find('i').mouseenter(function () {
                var val = parseInt($(this).attr('rating-value'), 10);
                highlightStars(val);
            }).click(function () {
                var val = parseInt($(this).attr('rating-value'), 10);
                self.value = val;
                $el.val(val).trigger('change');
                // if tipi was open because of an error, hide it!
                $container.tipi('hide');
            });

            $container.mouseleave(function () {
                highlightStars(self.value);
            });

            // finally update the DOM
            $el.after($container)
               .hide();

            // highlight a first time
            highlightStars(this.value);

            // finally give access to our container
            Plugin.prototype._$container = $container;

            return this;
        },

        val: function () {
            return this.value;
        },

        container: function () {
            return this._$container;
        }
    };

    // Instantiation or method call, accordingly
    $.fn[pluginName] = function (options) {
        var args = Array.prototype.slice.call(arguments),
            output;

        this.each(function() {
            var instance = $.data(this, 'plugin_' + pluginName),
                method;

            if (!instance) {
                $.data( this, 'plugin_' + pluginName, new Plugin(this, options));
            } else {
                method = args.shift();
                output = instance[method].apply(instance, args);
            }
        });

        // chain jQuery functions
        return output === undefined ? this : output;
    };

})(jQuery, window, document);

