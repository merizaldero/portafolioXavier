(function($) {
    'use strict';

    var xtt_draw = null;
    var xtt_canvas = null;
    var xtt_current_tool = 'select';
    var xtt_undo_stack = [];
    var xtt_max_undo = 20;

    $(document).ready(function() {
        if ( ! document.getElementById( 'xtt-drawing-area' ) ) {
            return;
        }

        xtt_init_editor();
        xtt_bind_toolbar();
        xtt_bind_canvas_events();
        xtt_load_existing_svg();
    });

    function xtt_init_editor() {
        var width = xtt_frontend_ajax.canvas_width || 800;
        var height = xtt_frontend_ajax.canvas_height || 600;

        xtt_draw = SVG( 'xtt-drawing-area' ).size( '100%', '100%' ).viewbox( 0, 0, width, height );

        xtt_draw.rect( width, height ).fill( '#f5f5f5' ).attr({ id: 'xtt-background' });

        xtt_canvas = xtt_draw.group().attr({ id: 'xtt-content-layer' });
    }

    function xtt_bind_toolbar() {
        $( '.xtt-tool-btn[data-tool]' ).on( 'click', function() {
            $( '.xtt-tool-btn' ).removeClass( 'xtt-active' );
            $( this ).addClass( 'xtt-active' );
            xtt_current_tool = $( this ).data( 'tool' );
        } );

        $( '#xtt-btn-delete' ).on( 'click', xtt_delete_selected );
        $( '#xtt-btn-undo' ).on( 'click', xtt_undo );
        $( '#xtt-btn-clear' ).on( 'click', xtt_clear_canvas );
        $( '#xtt-btn-resize' ).on( 'click', xtt_resize_canvas );
    }

    function xtt_bind_canvas_events() {
        $( '#xtt-drawing-area' ).on( 'click', function( e ) {
            if ( xtt_current_tool === 'select' ) {
                return;
            }

            var rect = this.getBoundingClientRect();
            var x = e.clientX - rect.left;
            var y = e.clientY - rect.top;

            var viewbox = xtt_draw.viewbox();
            var svg_x = x * ( viewbox.width / rect.width ) + viewbox.x;
            var svg_y = y * ( viewbox.height / rect.height ) + viewbox.y;

            var fill_color = $( '#xtt-fill-color' ).val();
            var stroke_color = $( '#xtt-stroke-color' ).val();
            var stroke_width = parseInt( $( '#xtt-stroke-width' ).val() ) || 2;
            var opacity = parseFloat( $( '#xtt-opacity' ).val() ) || 1;

            var new_element = null;

            switch ( xtt_current_tool ) {
                case 'rect':
                    new_element = xtt_canvas.rect( 100, 80 )
                        .move( svg_x - 50, svg_y - 40 )
                        .fill( fill_color )
                        .stroke({ color: stroke_color, width: stroke_width })
                        .opacity( opacity );
                    break;

                case 'circle':
                    new_element = xtt_canvas.circle( 80 )
                        .center( svg_x, svg_y )
                        .fill( fill_color )
                        .stroke({ color: stroke_color, width: stroke_width })
                        .opacity( opacity );
                    break;

                case 'ellipse':
                    new_element = xtt_canvas.ellipse( 60, 40 )
                        .center( svg_x, svg_y )
                        .fill( fill_color )
                        .stroke({ color: stroke_color, width: stroke_width })
                        .opacity( opacity );
                    break;

                case 'line':
                    new_element = xtt_canvas.line( svg_x, svg_y, svg_x + 100, svg_y + 100 )
                        .stroke({ color: stroke_color, width: stroke_width })
                        .opacity( opacity );
                    break;

                case 'polygon':
                    new_element = xtt_canvas.polygon( '0,0 50,-50 100,0 75,50 25,50' )
                        .move( svg_x - 50, svg_y - 25 )
                        .fill( fill_color )
                        .stroke({ color: stroke_color, width: stroke_width })
                        .opacity( opacity );
                    break;

                case 'text':
                    var text_content = prompt( 'Ingrese texto:', '' );
                    if ( text_content ) {
                        new_element = xtt_canvas.text( text_content )
                            .move( svg_x, svg_y )
                            .fill( fill_color )
                            .font({ size: 24, family: 'Arial' })
                            .opacity( opacity );
                    }
                    break;
            }

            if ( new_element ) {
                new_element.draggable();
                xtt_undo_stack.push( new_element );
                if ( xtt_undo_stack.length > xtt_max_undo ) {
                    xtt_undo_stack.shift();
                }
                xtt_current_tool = 'select';
                $( '.xtt-tool-btn' ).removeClass( 'xtt-active' );
                $( '#xtt-btn-select' ).addClass( 'xtt-active' );
            }
        } );

        $( '#xtt-frontend-form' ).on( 'submit', function() {
            xtt_save_svg();
        } );
    }

    function xtt_load_existing_svg() {
        var existing_svg = xtt_frontend_ajax.svg_content;
        if ( existing_svg && existing_svg.trim() !== '' ) {
            try {
                var temp_div = document.createElement( 'div' );
                temp_div.innerHTML = existing_svg;
                var svg_element = temp_div.querySelector( 'svg' );

                if ( svg_element ) {
                    var children = Array.from( svg_element.childNodes ).filter( function( node ) {
                        return node.nodeType === Node.ELEMENT_NODE;
                    } );

                    children.forEach( function( child ) {
                        if ( child.id !== 'xtt-background' ) {
                            xtt_canvas.add( child );
                        }
                    } );

                    $( xtt_canvas.node.querySelectorAll( '*' ) ).each( function() {
                        if ( ! $( this ).hasClass( 'xtt-background' ) ) {
                            try {
                                var svg_elem = SVG( this );
                                if ( typeof svg_elem.draggable === 'function' ) {
                                    svg_elem.draggable();
                                }
                            } catch ( e ) {
                            }
                        }
                    } );
                }
            } catch ( e ) {
                console.error( 'xtt: Error loading existing SVG:', e );
            }
        }
    }

    function xtt_save_svg() {
        var svg_content = xtt_draw.svg();
        $( '#xtt-svg-content' ).val( svg_content );
        $( '#xtt-canvas-width-hidden' ).val( $( '#xtt-canvas-width' ).val() );
        $( '#xtt-canvas-height-hidden' ).val( $( '#xtt-canvas-height' ).val() );

        var post_id = xtt_frontend_ajax.post_id;

        if ( ! post_id ) {
            return;
        }

        $.ajax({
            url: xtt_frontend_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'xtt_save_svg',
                nonce: xtt_frontend_ajax.nonce,
                post_id: post_id,
                svg_data: svg_content,
                width: parseInt( $( '#xtt-canvas-width' ).val() ) || 800,
                height: parseInt( $( '#xtt-canvas-height' ).val() ) || 600
            },
            success: function( response ) {
                if ( response.success ) {
                    console.log( 'xtt: SVG saved successfully' );
                }
            },
            error: function() {
                console.error( 'xtt: Error saving SVG' );
            }
        });
    }

    function xtt_delete_selected() {
        var selected = xtt_draw.select( '.selected' );
        if ( selected.length > 0 ) {
            selected.remove();
        }
    }

    function xtt_undo() {
        if ( xtt_undo_stack.length === 0 ) {
            return;
        }
        var element = xtt_undo_stack.pop();
        element.remove();
    }

    function xtt_clear_canvas() {
        if ( confirm( '¿Está seguro de limpiar todo el canvas?' ) ) {
            xtt_canvas.each( function( i, child ) {
                if ( child.attr( 'id' ) !== 'xtt-background' ) {
                    child.remove();
                }
            } );
            xtt_undo_stack = [];
        }
    }

    function xtt_resize_canvas() {
        var new_width = parseInt( $( '#xtt-canvas-width' ).val() ) || 800;
        var new_height = parseInt( $( '#xtt-canvas-height' ).val() ) || 600;

        xtt_draw.viewbox( 0, 0, new_width, new_height );

        var bg = xtt_draw.findOne( '#xtt-background' );
        if ( bg ) {
            bg.size( new_width, new_height );
        }
    }

    window.xtt_get_svg = function() {
        return xtt_draw ? xtt_draw.svg() : '';
    };

})(jQuery);
