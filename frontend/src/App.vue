<template>
  <div class="agm-container">
    <div class="agm-map">
      <ol-map ref="map" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 90vh">

        <ol-view
          ref="view"
          :center="center"
          :rotation="rotation"
          :zoom="zoom"
          :projection="projection"
        />

        <ol-layerswitcherimage-control />

        <ol-tile-layer ref="osmLayer" title="osm">
          <ol-source-osm />
        </ol-tile-layer>

        <ol-interaction-select
          @select="featureSelected"
          :condition="selectCondition"
        >
          <ol-style>
            <ol-style-stroke color="rgba(179,234,255,1)" :width="10"></ol-style-stroke>
            <ol-style-fill color="rgba(179,234,255,0.75)"></ol-style-fill>
            <ol-style-circle :radius="10">
              <ol-style-fill color="rgba(179,234,255,1)"></ol-style-fill>
            </ol-style-circle>
          </ol-style>
        </ol-interaction-select>

        <ol-vector-layer title="roads">
          <ol-source-vector
            ref="roads"
            url="http://127.0.0.1:8000/api/v1/roads"
            :format="geoJson"
            :projection="projection"
          />

          <ol-style>
            <ol-style-stroke color="red" :width="5"></ol-style-stroke>
            <ol-style-fill color="rgba(255,255,255,0.1)"></ol-style-fill>
          </ol-style>
        </ol-vector-layer>

        <ol-vector-layer title="road-cross">
          <ol-source-vector
            ref="roads"
            url="http://127.0.0.1:8000/api/v1/road-cross"
            :format="geoJson"
            :projection="projection"
          />

          <ol-style>
            <ol-style-stroke color="blue" :width="5"></ol-style-stroke>
            <ol-style-fill color="rgba(0,0,255,0.9)"></ol-style-fill>
          </ol-style>
        </ol-vector-layer>

        <ol-vector-layer title="lines">
          <ol-source-vector
            ref="roads"
            url="http://127.0.0.1:8000/api/v1/lines"
            :format="geoJson"
            :projection="projection"
          />

          <ol-style>
            <ol-style-stroke color="green" :width="5"></ol-style-stroke>
            <ol-style-fill color="rgba(255,255,255,0.1)"></ol-style-fill>
          </ol-style>
        </ol-vector-layer>

        <ol-vector-layer title="semaphores">
          <ol-source-vector
            ref="roads"
            url="http://127.0.0.1:8000/api/v1/semaphores"
            :format="geoJson"
            :projection="projection"
          />

          <ol-style>
            <ol-style-circle :radius="7">
              <ol-style-fill color="yellow"></ol-style-fill>
            </ol-style-circle>
          </ol-style>
        </ol-vector-layer>

        <ol-vector-layer title="gas-stations">
          <ol-source-vector
            ref="roads"
            url="http://127.0.0.1:8000/api/v1/gas-stations"
            :format="geoJson"
            :projection="projection"
          />

          <ol-style>
            <ol-style-circle :radius="7">
              <ol-style-fill color="orange"></ol-style-fill>
            </ol-style-circle>
          </ol-style>
        </ol-vector-layer>

      </ol-map>
    </div>
    <div class="agm-properties">
      <div v-for="(property, key) in properties" :key="key">
        <span>{{key}}: </span>{{property}}
      </div>
    </div>
  </div>
</template>
 
<script setup>
  import { ref, inject } from "vue"

  const center = ref([4338578.002510583, 5626177.3723523775])
  const projection = ref("EPSG:3857")
  const zoom = ref(6)
  const rotation = ref(0)

  const format = inject("ol-format")
  const geoJson = new format.GeoJSON()

  const selectConditions = inject("ol-selectconditions")

  const selectCondition = selectConditions.pointerMove

  const properties = ref({})

  function featureSelected(event) {
    const selected = event.selected
    if (!selected.length) return
    const {geometry, ...props} = selected[0].values_
    properties.value = props
  }

</script>
 
<style>
  .agm-container {
    display: flex;
    flex-direction: row;
  }
  .agm-map {
    flex-grow: 3;
  }
  .agm-properties {
    width: 240px;
    padding: 24px;
    font-family: sans-serif;
  }
</style>