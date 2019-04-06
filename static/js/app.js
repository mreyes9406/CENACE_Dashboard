// Get the function to insert interactive data into html file
Plotly.d3.csv('../../db/MDA_Prices.csv', function(err, rows) {
  //Unpack information. We need to change this later to the real endpoints but the logic for the frontend will be the same

  function unpack(rows, key) {
    return rows.map(function(row) {
      return row[key];
    });
  }

  var allDatesMDA = unpack(rows, 'Date'),
    allZonesMDA = unpack(rows, 'Zone'),
    allLMPMDA = unpack(rows, 'LMP'),
    allEnergyMDA = unpack(rows, 'Energy_Cost'),
    allLossesMDA = unpack(rows, 'Losses_Cost'),
    allCongestionMDA = unpack(rows, 'Congestion_Cost'),
    allMovingAverageMDA = unpack(rows, 'Moving_Average'),
    listofDates = [],
    listofZones = ([].currentDate = []),
    currentLMPMDA = [],
    currentEnergyMDA = [],
    currentLossesMDA = [],
    currentCongestionMDA = [],
    currentAveragesMDA = [];

  for (var i = 0; i < 32; i++) {
    if (listofDates.indexOf(allDatesMDA[i]) === -1) {
      listofDates.push(allDatesMDA[i]);
    }
  }

  allZonesMDA.forEach(element => {
    if (listofZones.indexOf(element) === -1) {
      listofZones.push(element);
    }
  });

  function avgValues(valuesArray) {
    var sumArray = 0;
    for (var i = 0; i < valuesArray.length; i++) {
      var num = parseInt(valuesArray[i], 10);
      sumArray = sumArray + num;
    }
    return sumArray / valuesArray.length;
  }

  function minValues(valuesArray) {
    return Math.min(...valuesArray);
  }

  function maxValues(valuesArray) {
    return Math.max(...valuesArray);
  }

  function getDateData(chosenDate) {
    currentEnergyMDA = [];
    currentLossesMDA = [];
    currentCongestionMDA = [];
    for (var i = 0; i < allDatesMDA.length; i++) {
      if (allDatesMDA[i] === chosenDate) {
        currentEnergyMDA.push(allEnergyMDA[i]);
        currentLossesMDA.push(allLossesMDA[i]);
        currentCongestionMDA.push(allCongestionMDA[i]);
      }
    }
  }

  function getZoneData(chosenZone) {
    currentAveragesMDA = [];

    for (var i = 7; i < allMovingAverageMDA.length; i++) {
      if (allZonesMDA[i] === chosenZone) {
        currentAveragesMDA.push(allMovingAverageMDA[i]);
      }
    }
  }

  //CREATE INTERACTIVE BAR CHART
  // Default Date Data
  setBarPlot(listofDates[0]);

  //Function to set the interactive bar chart
  function setBarPlot(chosenDate) {
    getDateData(chosenDate);

    var avgEnergyMDA = avgValues(currentEnergyMDA);
    var avgLossesMDA = avgValues(currentLossesMDA);
    var avgCongestionMDA = avgValues(currentCongestionMDA);
    var maxEnergyMDA = maxValues(currentEnergyMDA);
    var minEnergyMDA = maxValues(currentEnergyMDA);
    var maxLossesMDA = maxValues(currentLossesMDA);
    var minLossesMDA = minValues(currentLossesMDA);
    var maxCongestionMDA = maxValues(currentCongestionMDA);
    var minCongestionMDA = minValues(currentCongestionMDA);

    var trace1 = {
      x: ['Energy', 'Losses', 'Congestion'],
      y: [avgEnergyMDA, avgLossesMDA, avgCongestionMDA],
      text: [
        'Max. Energy Cost:<br>' +
          '$' +
          maxEnergyMDA +
          '/MWh<br>' +
          'Min. Energy Cost:<br>' +
          '$' +
          minEnergyMDA +
          '/MWh',
        'Max. Losses Cost:<br>' +
          '$' +
          maxLossesMDA +
          '/MWh<br>' +
          'Min. Losses Cost:<br>' +
          '$' +
          minLossesMDA +
          '/MWh',
        'Max. Congestion Cost:<br>' +
          '$' +
          maxCongestionMDA +
          '/MWh<br>' +
          'Min. Congestion Cost:<br>' +
          '$' +
          minCongestionMDA +
          '/MWh',
      ],
      hoverinfo: 'text',
      hoverlabel: {
        bgcolor: '#696969',
        font: { color: 'white' },
      },
      type: 'bar',
    };

    var data = [trace1];

    var layout = {
      title:
        'Average cost of energy components' + '<br>' + 'during: ' + chosenDate,
      annotations: [
        {
          text: 'Select the day you want to explore from the menu below',
          font: {
            size: 13,
            color: '#A9A9A9',
          },
          showarrow: false,
          align: 'center',
          x: 0.5,
          y: 1.07,
          xref: 'paper',
          yref: 'paper',
        },
        {
          text: 'All costs are in $MXN per MWh',
          font: {
            size: 11,
            color: '#696969',
          },
          showarrow: false,
          align: 'center',
          x: 0.5,
          y: -0.2,
          xref: 'paper',
          yref: 'paper',
        },
      ],
      yaxis: {
        title: '$MXN per MWh',
        showline: true,
        showgrid: true,
        showticklabels: true,
        linecolor: '#696969',
        linewidth: 1,
        autotick: true,
        ticks: 'outside',
        tickcolor: '#696969',
        tickwidth: 2,
        ticklen: 3,
        tickfont: {
          family: 'Arial',
          size: 9,
          color: 'rgb(82, 82, 82)',
        },
      },
      height: 500,
      //width: "auto",
    };

    Plotly.newPlot('bar', data, layout, { responsive: true });
  }

  var dateSelector = document.querySelector('.datedata');

  function assignOptionsDate(textArray, selector) {
    for (var i = 0; i < textArray.length; i++) {
      var currentOption = document.createElement('option');
      currentOption.text = textArray[i];
      selector.appendChild(currentOption);
    }
  }

  assignOptionsDate(listofDates, dateSelector);

  function updateDate() {
    setBarPlot(dateSelector.value);
  }

  dateSelector.addEventListener('change', updateDate, false);

  //CREATE INTERACTIVE LINE CHART
  // Default Zone Data
  setLinePlot(listofZones[0]);

  //Function to build interactive line chart
  function setLinePlot(chosenZone) {
    getZoneData(chosenZone);

    var movingDates = listofDates.slice(7, listofDates.lenght);

    var text=[];

    for (var n = 0; n < Object.keys(movingDates).length; n++) {
      var number = parseFloat(currentAveragesMDA[n]);
      var threedigit = number.toFixed(3);
      text.push(movingDates[n] + "<br>Moving average: <br>" + "$" + threedigit +"/MWh") 
    };

    var trace1 = {
      x: movingDates,
      y: currentAveragesMDA,
      text: text,
      hoverinfo: "text",
      type: 'scatter',
      name: 'MDA',
    };

    var data = [trace1];

    var layout = {
      title:
        'Running Average Locational Marginal Prices' +
        '<br>' +
        'Zone: ' +
        chosenZone,
      annotations: [
        {
          text: 'Select the zone you want to explore from the menu below',
          font: {
            size: 13,
            color: '#A9A9A9',
          },
          showarrow: false,
          align: 'center',
          x: 0.5,
          y: 1.12,
          xref: 'paper',
          yref: 'paper',
        },
      ],
      xaxis: {
        title: 'Day',
        showline: true,
        showgrid: true,
        showticklabels: true,
        linecolor: '#696969',
        linewidth: 1,
        autotick: false,
        ticks: 'outside',
        tickcolor: '#696969',
        tickwidth: 2,
        ticklen: 3,
        tickfont: {
          family: 'Arial',
          size: 9,
          color: 'rgb(82, 82, 82)',
        },
      },
      yaxis: {
        title: '$MXN per MWh',
        showline: true,
        showgrid: true,
        showticklabels: true,
        linecolor: '#696969',
        linewidth: 1,
        autotick: true,
        ticks: 'outside',
        tickcolor: '#696969',
        tickwidth: 2,
        ticklen: 3,
        tickfont: {
          family: 'Arial',
          size: 9,
          color: 'rgb(82, 82, 82)',
        },
      },
      height: 400,
      //width: 1150,
    };

    Plotly.newPlot('line', data, layout, { responsive: true });
  }

  var zoneSelector = document.querySelector('.zonedata');

  function assignOptionsZone(textArray, selector) {
    for (var i = 0; i < textArray.length; i++) {
      var currentOption = document.createElement('option');
      currentOption.text = textArray[i];
      selector.appendChild(currentOption);
    }
  }

  assignOptionsZone(listofZones, zoneSelector);

  function updateZone() {
    setLinePlot(zoneSelector.value);
  }

  zoneSelector.addEventListener('change', updateZone, false);
});

//CREATE INTERACTIVE MAP OF BAJA CALIFORNIA USING LEAFLET

var lightmap = L.tileLayer(
  'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}',
  {
    attribution:
      'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.light',
    accessToken:
      'pk.eyJ1IjoibWFyaWFuYWptdHoiLCJhIjoiY2p0Z2lnODB0MGZrODRhcDhyczZwbm1qbiJ9.oYT0cdl3p1en531BVozZtA',
  },
);

//LayerGroups we'll be using
var layers = {
  ENSENADA: new L.LayerGroup(),
  MEXICALI: new L.LayerGroup(),
  SANLUIS: new L.LayerGroup(),
  TIJUANA: new L.LayerGroup(),
};

// Create the tile layer that will be the background of our map
var map = L.map('map-id', {
  center: [30.467, -115.1],
  zoom: 6.4,
  layers: [
    layers.ENSENADA,
    layers.MEXICALI,
    layers.SANLUIS,
    layers.TIJUANA
    ],
});

// Add our 'lightmap' tile layer to the map
lightmap.addTo(map);

//Overlays object to add to layer control
var overlays = {
  "ENSENADA": layers.ENSENADA,
  "MEXICALI": layers.MEXICALI,
  "SANLUIS": layers.SANLUIS,
  "TIJUANA": layers.TIJUANA,
};

// Create a control for our layers, add our overlay layers to it
L.control.layers(null, overlays).addTo(map);

d3.json('../../db/BC_Geodata.json').then(function(infoMap) {
  var municipalitiesInfo = infoMap.features;

  var mapCoordinates;

  var zoneCode;

  var latlngs;

  var tijuanaCoord = [];

  for (var n = 0; n < municipalitiesInfo.length; n++) {
    // Create a new station object with properties of both station objects
    var feature = Object.assign({}, municipalitiesInfo[n]);

    if (feature.properties.mun_name === "Ensenada"){
      mapCoordinates = feature.geometry.coordinates;
      latlngs = [mapCoordinates].flat(2).map(c => c.map(c => [c[1], c[0]]));
      zoneCode = "ENSENADA";
      var polygon = L.polygon(latlngs, {
        fillColor: 'red',
        weight: 0,
        opacity: 0.5,
        color: 'red',  
        fillOpacity: 0.5});
      polygon.addTo(layers[zoneCode]);
      polygon.bindPopup("Zona de Carga: " + zoneCode);
    }

    else if (feature.properties.mun_name === "Mexicali"){
      mapCoordinates = feature.geometry.coordinates;
      latlngs = [mapCoordinates].flat(2).map(c => c.map(c => [c[1], c[0]]));
      zoneCode = "MEXICALI";
      var polygon = L.polygon(latlngs, {
        fillColor: 'blue',
        weight: 0,
        opacity: 0.5,
        color: 'blue',  
        fillOpacity: 0.5});
      polygon.addTo(layers[zoneCode]);
      polygon.bindPopup("Zona de Carga: " + zoneCode);
    }

    else if (feature.properties.mun_name === "San Luis Río Colorado"){
      mapCoordinates = feature.geometry.coordinates;
      latlngs = [mapCoordinates].flat(2).map(c => c.map(c => [c[1], c[0]]));
      zoneCode = "SANLUIS";
      var polygon = L.polygon(latlngs, {
        fillColor: 'green',
        weight: 0,
        opacity: 0.5,
        color: 'green',  
        fillOpacity: 0.5});
      polygon.addTo(layers[zoneCode]);
      polygon.bindPopup("Zona de Carga: " + zoneCode);
    }     

    else {
      mapCoordinates = feature.geometry.coordinates;
      tijuanaCoord.push(mapCoordinates);
      latlngs = [tijuanaCoord].flat(2).map(c => c.map(c => [c[1], c[0]]));
      zoneCode = "TIJUANA";
      var polygon = L.polygon(latlngs, {
        fillColor: 'yellow',
        weight: 0,
        opacity: 0.5,
        color: 'yellow',  
        fillOpacity: 0.5});
      polygon.addTo(layers[zoneCode]);
      polygon.bindPopup("Zona de Carga: " + zoneCode);
    } 
  };

  var legend = L.control({position: 'bottomcenter'});

  legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        labels = ['<strong> Promedios por Zona de Carga </strong>'];
    div.innerHTML += '<b>Legend Title</b><br>'
    return div;
  };

});
