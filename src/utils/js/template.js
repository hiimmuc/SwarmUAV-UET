
{% macro header(this, kwargs) %}
    <meta name="viewport" content="width=device-width,
        initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <style>
        #{{ this.get_name() }} {
            position: {{this.position}};
            width: {{this.width[0]}}{{this.width[1]}};
            height: {{this.height[0]}}{{this.height[1]}};
            left: {{this.left[0]}}{{this.left[1]}};
            top: {{this.top[0]}}{{this.top[1]}};
        }
        .leaflet-container { font-size: {{this.font_size}}; }
    </style>
{% endmacro %}

{% macro html(this, kwargs) %}
    <div class="folium-map" id={{ this.get_name()|tojson }} ></div>
{% endmacro %}

// {% macro script("text/javascript", "./qwebchannel.js") %}

{% macro script(this, kwargs) %}
    var {{ this.get_name() }} = L.map(
        {{ this.get_name()|tojson }},
        {
            center: {{ this.location|tojson }},
            crs: L.CRS.{{ this.crs }},
            {%- for key, value in this.options.items() %}
            {{ key }}: {{ value|tojson }},
            {%- endfor %}
        }
    );

    {%- if this.control_scale %}
    L.control.scale().addTo({{ this.get_name() }});
    {%- endif %}

    {%- if this.zoom_control_position %}
    L.control.zoom( { position: {{ this.zoom_control|tojson }} } ).addTo({{ this.get_name() }});
    {%- endif %}

    {% if this.objects_to_stay_in_front %}
    function objects_in_front() {
        {%- for obj in this.objects_to_stay_in_front %}
            {{ obj.get_name() }}.bringToFront();
        {%- endfor %}
    };
    {{ this.get_name() }}.on("overlayadd", objects_in_front);
    $(document).ready(objects_in_front);
    {%- endif %}

{% endmacro %}
        