(function($) {
    'use strict';

    window.xtt_convert_svg_to_png = function( svg_data, width, height, post_id ) {
        if ( ! svg_data || ! width || ! height || ! post_id ) {
            console.error( 'xtt-converter: Missing required parameters' );
            return;
        }

        var canvas = document.createElement( 'canvas' );
        canvas.width = width;
        canvas.height = height;

        var ctx = canvas.getContext( '2d' );

        var img = new Image();
        var svg_blob = new Blob( [ svg_data ], { type: 'image/svg+xml;charset=utf-8' } );
        var url = URL.createObjectURL( svg_blob );

        img.onload = function() {
            ctx.clearRect( 0, 0, width, height );
            ctx.drawImage( img, 0, 0, width, height );

            var png_data_url = canvas.toDataURL( 'image/png' );

            xtt_save_png_to_server( png_data_url, post_id );

            URL.revokeObjectURL( url );
        };

        img.onerror = function() {
            console.error( 'xtt-converter: Failed to load SVG for conversion' );
        };

        img.src = url;
    };

    function xtt_save_png_to_server( png_data_url, post_id ) {
        $.ajax({
            url: xtt_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'xtt_save_png',
                nonce: xtt_ajax.nonce,
                post_id: post_id,
                png_data: png_data_url
            },
            success: function( response ) {
                if ( response.success ) {
                    console.log( 'xtt-converter: PNG saved successfully' );
                    xtt_update_preview( png_data_url );
                } else {
                    console.error( 'xtt-converter: Error saving PNG:', response.data.message );
                }
            },
            error: function() {
                console.error( 'xtt-converter: AJAX error saving PNG' );
            }
        });
    }

    function xtt_update_preview( png_data_url ) {
        var preview_container = $( '#xtt-preview-container' );
        if ( preview_container.length ) {
            preview_container.html( '<img id="xtt-preview-img" src="' + png_data_url + '" alt="Preview PNG">' );
        }
    }

    window.xtt_convert_and_save = function() {
        var svg_content = '';
        if ( typeof xtt_get_svg === 'function' ) {
            svg_content = xtt_get_svg();
        }

        if ( ! svg_content ) {
            console.error( 'xtt-converter: No SVG content available' );
            return;
        }

        var width = parseInt( $( '#xtt-canvas-width' ).val() ) || 800;
        var height = parseInt( $( '#xtt-canvas-height' ).val() ) || 600;
        var post_id = xtt_ajax.post_id;

        if ( ! post_id ) {
            console.error( 'xtt-converter: No post ID available' );
            return;
        }

        window.xtt_convert_svg_to_png( svg_content, width, height, post_id );
    };

})(jQuery);
