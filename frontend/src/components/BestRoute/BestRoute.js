import { Link } from "react-router-dom";
import Header from "../Header/Header";
import Button from "../Button/Button";
import trashIcon from "../../images/trash-icon.svg";
import stub from "../../images/stub-2.svg";
import api from "../../utils/api";
import "./BestRoute.css";

const { ymaps } = window;

function BestRoute() {

  ymaps.ready(init);

  function init() {
    let to;

    api
    .getShortest()
    .then((data) => {
      to = data[0];
      var pointA = [55.75974142552072, 37.610742623045255],
        pointB = [to.longitude, to.latitude],
        multiRoute = new ymaps.multiRouter.MultiRoute(
          {
            referencePoints: [pointA, pointB],
            params: {
              routingMode: "pedestrian",
              results: 1,
            },
          },
          {
            boundsAutoApply: true,
          }
        );

      var map = new ymaps.Map("map", {
        center: [55.739625, 37.5412],
        zoom: 12,
        controls: ["zoomControl"],
      });

      map.geoObjects.add(multiRoute);
      })
    .catch((error) => {
      console.log(error);
    });
  }


  return (
    <div className="best-route">
      <Header />
      <div className="best-route__button-list">
        <Button text="Поделиться" />
        <Link to="/" style={{ color: "none", textDecoration: "none" }}>
          <Button type="round" icon={trashIcon} />
        </Link>
      </div>
      <img className="best-route__stub" src={stub} alt="" />
      <div id="map" className="best-route__map"></div>
    </div>
  );
}

export default BestRoute;
