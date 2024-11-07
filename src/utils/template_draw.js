{% macro script(this, kwargs) %}
    var options = {
        position: {{ this.position|tojson }},
        draw: {{ this.draw_options|tojson }},
        edit: {{ this.edit_options|tojson }},
    }

    var map = {{ this._parent.get_name() }};

    
    {%- if this.feature_group  %}
        var drawnItems_{{ this.get_name() }} =
            {{ this.feature_group.get_name() }};
    {%- else %}
        // FeatureGroup is to store editable layers.
        var drawnItems_{{ this.get_name() }} =
            new L.featureGroup().addTo(
                {{ this._parent.get_name() }}
            );
    {%- endif %}

    options.edit.featureGroup = drawnItems_{{ this.get_name() }};
    var {{ this.get_name() }} = new L.Control.Draw(
        options
    ).addTo( {{this._parent.get_name()}} );

    map.on(L.Draw.Event.CREATED, function(e) {
        var layer = e.layer,
            type = e.layerType;
        var coords = JSON.stringify(layer.toGeoJSON());
        {%- if this.show_geometry_on_click %}
        layer.on('click', function() {
            alert(coords);
            console.log(coords);
        });
        {%- endif %}

        {%- for event, handler in this.on.items()   %}
        layer.on(
            "{{event}}",
            {{handler}}
        );
        {%- endfor %}
        drawnItems_{{ this.get_name() }}.addLayer(layer);
    });

    {{ this._parent.get_name() }}.on('draw:created', function(e) {
        drawnItems_{{ this.get_name() }}.addLayer(e.layer);
    });

    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.qtWidget = channel.objects.qtWidget;
        map.on('dragend', function () {
            center = map.getCenter();
            qtWidget.mapMoved(center.lat, center.lng);
        });

        map.on('click', function (ev) {
            qtWidget.mapLeftClicked(ev.latlng.lat, ev.latlng.lng);
        });

        map.on('dblclick', function (ev) {
            qtWidget.mapDoubleClicked(ev.latlng.lat, ev.latlng.lng);
        });

        map.on('contextmenu', function (ev) {
            qtWidget.mapRightClicked(ev.latlng.lat, ev.latlng.lng);
        });
        map.on(L.Draw.Event.CREATED, function (e) {
            var type = e.layerType,
                layer = e.layer;
            var geojsonData = JSON.stringify(layer.toGeoJSON());
            qtWidget.geoJsonHandle(geojsonData);
        });
        
    });

{% endmacro %}
