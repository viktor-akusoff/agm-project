<template>
  <div class="agm-container">
    <div class="agm-map">
      <ol-map ref="mapRef" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 90vh" @dblclick="showPanorama = true">

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

        <ol-overlay
          v-if="showTooltip"
          :position="helpTooltipCoord"
          :offset="[0, 15]"
          positioning="top-center"
        >
          <div class="tooltip">
            {{ helpTooltipText }}
          </div>
        </ol-overlay>

        <ol-interaction-select
          @select="featureSelected"
          :condition="clickCondition"
        >
          <ol-style>
            <ol-style-stroke color="rgba(216,183,255,1)" :width="10"></ol-style-stroke>
            <ol-style-fill color="rgba(216,183,255,0.75)"></ol-style-fill>
            <ol-style-circle :radius="10">
              <ol-style-fill color="rgba(216,183,255,1)"></ol-style-fill>
            </ol-style-circle>
          </ol-style>      
        </ol-interaction-select>

        <ol-interaction-select
          @select="toggleTooltip"
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
  <div class="shadow-overlay" v-show="showPanorama">
    <div class="window">
      <button @click="showPanorama = false">x</button>
      <div id="viewer3d" style="width: 100%; height: 100%;"></div>
    </div>
  </div>
</template>
 
<script setup>
  import { ref, inject, onMounted } from "vue"

  const mapRef = ref(null)

  const showPanorama = ref(false)

  const center = ref([4338578.002510583, 5626177.3723523775])
  const projection = ref("EPSG:3857")
  const zoom = ref(7)
  const rotation = ref(0)

  const format = inject("ol-format")
  const geoJson = new format.GeoJSON()

  const selectConditions = inject("ol-selectconditions")

  const selectCondition = selectConditions.pointerMove
  const clickCondition = selectConditions.click

  const properties = ref({})

  const helpTooltipCoord = ref(null);
  const helpTooltipText = ref("TEST");

  function featureSelected(event) {
    const selected = event.selected
    if (!selected.length) return
    const {geometry, ...props} = selected[0].values_
    properties.value = props
  }

  const showTooltip = ref(false)

  function toggleTooltip(event) {
    if (event.selected.length)
      showTooltip.value = true
    else
      showTooltip.value = false
  }

  function showHelpInfoOnPointermove(evt) {
    if (evt.dragging) {
      return;
    }
    helpTooltipText.value = evt.coordinate;
    helpTooltipCoord.value = evt.coordinate;
  }

  onMounted(() => {
    mapRef.value?.map.on("pointermove", showHelpInfoOnPointermove);
    mapRef.value?.map.getViewport().addEventListener("mouseout", function () {
      helpTooltipCoord.value = null;
      helpTooltipText.value = "";
    });
    mapRef.value?.map.getInteractions().forEach(interaction => {
      if (interaction?.constructor.name === "DoubleClickZoom") {
        mapRef.value.map.removeInteraction(interaction);
      }
    });
  });



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
  .tooltip {
    background: rgb(187, 255, 223);
    font-family: sans-serif;
    padding: 5px;
    border-radius: 5px;
  }
  .shadow-overlay {
    background-color: rgba(0,0,0,0.5);
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    z-index: 1000;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }
  .window {
    position: relative;
    border-radius: 5px;
    background-color: white;
    padding: 36px;
    width: 75vw;
    height: 75vh;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .window button {
    background: none;
    border: none;
    font-family: sans-serif;
    font-size: 24px;
    color: #121212;
    cursor: pointer;
    position: absolute;
    top: 8px;
    right: 8px;
  }
</style>