import { Link } from "react-router-dom";
import React from "react";
import Button from "../Button/Button";
import Header from "../Header/Header";
import chatIcon from "../../images/chat-icon.svg";
import api from "../../utils/api";
import "./Main.css";

const { ymaps } = window;

function Main() {
  // const [branches, setBranches] = React.useState([]);

  // React.useEffect(() => {
  //   api
  //     .getBranches()
  //     .then((data) => {
  //       setBranches(data);
  //       ymaps.ready(init); // Инициализация карты после получения данных
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
  // }, []);

  // function init() {
  //   var map = new ymaps.Map("map", {
  //     center: [55.76, 37.64],
  //     zoom: 10,
  //   });

  //   map.geoObjects.add(
  //     new ymaps.Placemark([branches[0].latitude, branches[0].longitude], {
  //       hintContent: 'Тестовая метка',
  //     })
  //   );

  //   console.log(branches);
  //   branches.forEach((branch) => {
  //     console.log("Я тут");
  //     map.geoObjects.add(
  //       new ymaps.Placemark([branch.latitude, branch.longitude], {
  //         hintContent: 'Тестовая метка',
  //       })
  //     );
  //   });

  //   // branches.forEach((branch) => {
  //   //   map.geoObjects.add(
  //   //     new ymaps.Placemark(
  //   //       [branch.latitude, branch.longitude],
  //   //       {
  //   //         data: [
  //   //           { weight: (branch.load / 3) * 100, color: "#0663EF" },
  //   //           { weight: 100 - (branch.load / 3) * 100, color: "#FFFFFF" },
  //   //         ],
  //   //       },
  //   //       {
  //   //         iconLayout: "default#pieChart",
  //   //         iconPieChartRadius: 30,
  //   //         iconPieChartCoreRadius: 10,
  //   //         iconPieChartCoreFillStyle: "#ffffff",
  //   //         iconPieChartStrokeStyle: "#ffffff",
  //   //         iconPieChartStrokeWidth: 3,
  //   //         iconPieChartCaptionMaxWidth: 200,
  //   //       }
  //   //     )
  //   //   );
  //   // });
  // }

ymaps.ready(init);

function init () {
    var myMap = new ymaps.Map('map', {
            center: [55.76, 37.64],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        }),
        objectManager = new ymaps.ObjectManager({
            // Чтобы метки начали кластеризоваться, выставляем опцию.
            clusterize: true,
            // ObjectManager принимает те же опции, что и кластеризатор.
            gridSize: 32,
            clusterDisableClickZoom: true
        });

    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    objectManager.clusters.options.set('iconColor', '#0663EF');
    objectManager.objects.options.set('iconColor', '#0663EF');
    myMap.geoObjects.add(objectManager);

    api
      .getBranches()
      .then((data) => {
        //setBranches(data);
        console.log(convertToFeatureCollection(data))
        objectManager.add(convertToFeatureCollection(data)); // Инициализация карты после получения данных
      })
      .catch((error) => {
        console.log(error);
      });
}

function convertToFeatureCollection(data) {
  return {
      type: "FeatureCollection",
      features: data.map(item => ({
          type: "Feature",
          id: item.id,
          geometry: {
              type: "Point",
              coordinates: [item.longitude, item.latitude]
          },
          properties: {
              balloonContentHeader: `<font size=3><b>${item.name}</b></font>`,
              balloonContentBody: `<p>Адрес: ${item.address}</p><p>Загрузка: ${item.load}%</p>`,
              balloonContentFooter: "<font size=1>Дополнительная информация</font>",
              clusterCaption: `<strong>${item.name}</strong>`,
              hintContent: `<strong>${item.name}</strong>`
          }
      }))
  };
}

  return (
    <div className="main">
      <Header
        info={{ text: "Cредняя загруженность 75%", color: "#CA181FB2" }}
      />
      <div className="main__button-container">
        <Link to="/chat" style={{ color: "none", textDecoration: "none" }}>
          <Button text="Подобрать отделение" icon={chatIcon} />
        </Link>
      </div>
      <div id="map" className="main__map"></div>
    </div>
  );
}

export default Main;
