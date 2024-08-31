<template>
  <div class="agm-container">
    <div class="agm-map">
      <ol-map ref="mapRef" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 90vh" @dblclick="togglePanorama">

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
      <button class="close" @click="showPanorama = false">x</button>
      <div ref="canvasContainer" style="width: 100%; height: 100%"></div>
      <button @click="resetCamera">Домой</button>
    </div>
  </div>
</template>
 
<script setup>
  import { ref, inject, onMounted, watch, nextTick } from "vue"
  import axios from 'axios';
  import * as THREE from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

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

  const canvasContainer = ref(null);
  let animationId = null;
  let scene, camera, renderer, controls, geometry, textureLoader, texture, material, animate, sphere, lineMaterial, lineGeometry;
  let geometryList = []

  function resetCamera() {
    camera.position.z = 5;
    camera.rotation.x = 0;
    camera.rotation.y = 0;
    camera.rotation.z = 0;
  }

  watch(showPanorama, (newValue) => {
    if (newValue == false) {
      cancelAnimationFrame(animationId);
      if (renderer) renderer.dispose();
      if (scene) scene.clear();
      if (camera) camera = null;
      if (controls) controls.dispose();
      if (geometry) geometry.dispose();
      if (texture) texture.dispose();
      if (material) material.dispose();
      if (lineMaterial) lineMaterial.dispose();
      if (lineGeometry) lineGeometry.dispose();
      geometryList = []
      canvasContainer.value.innerHTML = '';
    }
  })

  async function fetchLines(center, y) {
    const lineMaterial = new THREE.MeshBasicMaterial({ 
      color: 0x00aa00, 
      depthTest: false 
    });
    const response = await axios('http://127.0.0.1:8000/api/v1/lines?epsg=3857')
    let features = response.data.features
    features.forEach((feature)=>{
      let processed_coordinates = []
      feature.geometry.coordinates.forEach((coordinate) => {
        let processed_coordinate = coordinate
        processed_coordinate[0] -= center[0]
        processed_coordinate[2] = processed_coordinate[1] - center[1]
        processed_coordinate[1] = y
        const temp = processed_coordinate[0]
        processed_coordinate[0] = processed_coordinate[2]
        processed_coordinate[2] = temp
        if (Math.abs(processed_coordinate[0]) < 1000 && Math.abs(processed_coordinate[2]) < 1000) {
          processed_coordinates.push(new THREE.Vector3(...processed_coordinate))
        }
      })
      if (processed_coordinates.length > 0) {
        geometryList.push(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(processed_coordinates), 1024, 0.5, 8, false), lineMaterial))
      }
    })
  }

  async function fetchPoly(center, y) {
    const material = new THREE.MeshBasicMaterial({ 
      color: 0x0000ff, 
      side: THREE.DoubleSide, // Fill both sides of the shape
      depthTest: false        // Optional: If you want it to always be on top
    });

    const response = await axios('http://127.0.0.1:8000/api/v1/road-cross?epsg=3857');
    let features = response.data.features;

    features.forEach((feature) => {
      let shape = new THREE.Shape();
      feature.geometry.coordinates[0].forEach((coordinate, index) => {
        let processed_coordinate = [...coordinate];
        processed_coordinate[0] -= center[0];
        processed_coordinate[2] = processed_coordinate[1] - center[1];
        processed_coordinate[1] = y;

        const [x, _, z] = processed_coordinate;

        if (Math.abs(x) < 1000 && Math.abs(z) < 1000) {
          if (index === 0) {
            shape.moveTo(z, x);
          } else {
            shape.lineTo(z, x); 
          }
        }
      });

      if (shape.getPoints().length > 2) {
        let geometryShape = new THREE.ShapeGeometry(shape);
        let meshShape = new THREE.Mesh(geometryShape, material);
        meshShape.rotateX(Math.PI/2)
        meshShape.position.y = y
        geometryList.push(meshShape);
      }
    });
  }

  async function buildPanorama() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(
      75,
      canvasContainer.value.clientWidth / canvasContainer.value.clientHeight,
      0.1,
      50
    );
    renderer = new THREE.WebGLRenderer();

    controls = new OrbitControls(camera, renderer.domElement);

    controls.maxDistance = 7;
    
    renderer.setSize(
      canvasContainer.value.clientWidth,
      canvasContainer.value.clientHeight
    );
    canvasContainer.value.appendChild(renderer.domElement);

    geometry = new THREE.SphereGeometry(8, 128, 128);

    textureLoader = new THREE.TextureLoader();
    texture = await textureLoader.load('http://127.0.0.1:8000/api/v1/panorama'); // Replace with your texture path

    texture.wrapS = THREE.RepeatWrapping;
    texture.repeat.x = - 1;

    material = new THREE.MeshBasicMaterial({ map: texture });

    material.side = THREE.DoubleSide;

    sphere = new THREE.Mesh(geometry, material);
    
    scene.add(sphere);

    resetCamera();

    animate = function () {
      animationId = requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };

    animate();
  }

  async function togglePanorama(event) {
    showPanorama.value = true
    nextTick(async () => {
      await buildPanorama()
      await fetchLines(event.coordinate, -8)
      await fetchPoly(event.coordinate, -8)
        geometryList.forEach((g) => {
        scene.add(g)
      })
    })
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .window .close {
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